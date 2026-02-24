Antes de criar a lambda function, vou preparar a role e a policy que ela vai utilizar. Como as policies podem ser lidas em json, criei um arquivo chamado [role-policy-iot-lambda.json](../../backend/role-policy-iot-lambda.json) para colocar os serviços que vou permitir. O arquivo contém:

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "lambda.amazonaws.com",
          "iot.amazonaws.com"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Com isso, o AWS IoT e o Lambda podem assumir essa role para executar ações com as permissões que estiverem anexadas a ela. Rodei o comando para criar a role:

`aws iam create-role --role-name role-iot-lambda --assume-role-policy-document file://backend/role-policy-iot-lambda.json`

![Role in Console](../img/05-create-role.png)

Também criei o json da policy de permissão em [permission-policy.json](../../backend/permission-policy.json):

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "StmtDynamoDBAccess",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:Scan",
        "dynamodb:UpdateItem"
      ],
      "Effect": "Allow",
      "Resource": "*"
    },
    {
      "Sid": "StmtIoTAccess",
      "Action": [
        "iot:Connect",
        "iot:Publish",
        "iot:Receive",
        "iot:Subscribe"
      ],
      "Effect": "Allow",
      "Resource": "*"
    },
    {
      "Sid": "StmtLogsAccess",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```

Depois, executei o comando:

`aws iam create-policy --policy-name permission-policy-lambda --policy-document file://backend/permission-policy-lambda.json`

![Policy in console](../img/06-permission-policy.png)

Anexei a policy na role usando o comando:

`aws iam attach-role-policy --role-name role-iot-lambda --policy-arn arn:aws:iam::xxxxxxxxxxxxxxx:policy/permission-policy-lambda`

![Policy attached to role in console](../img/07-attached-entity.png)

Para criar o Lambda por CLI, preparei a function em um arquivo.py: [lambda-function.py](../../backend/lambda-function.py). O comando para criar a function não aceita .py, para contornar isso preciso criar um pacote de deploy .zip. Tudo que fiz foi zippar o .py usando winrar e preparar o comando com o arn da role e o zip-file:

```
aws lambda create-function \
  --function-name anomaly-detector \
  --runtime python3.9 \
  --role arn:aws:iam::xxxxxxxxxxxxx:role/role-iot-lambda \
  --handler lambda_function.lambda_handler \
  --timeout 15 \
  --memory-size 512 \
  --zip-file fileb://backend/lambda_function.zip
```

One-line:

`aws lambda create-function --function-name anomaly-detector --runtime python3.9 --role arn:aws:iam::xxxxxxxxxxxxx:role/role-iot-lambda --handler lambda_function.lambda_handler --timeout 15 --memory-size 512 --zip-file fileb://backend/lambda-function.zip`

![Lambda function page](../img/08-lambda-function-created.png)

![Lambda code source](../img/09-lambda-code-source.png)

Rodei um teste com o input:

```
{
  "PrinterId": "Printer1",
  "data": {
    "type": "temperature",
    "value": 85
  }
}
```

![Lambda code test output](../img/10-lambda-code-test.png)