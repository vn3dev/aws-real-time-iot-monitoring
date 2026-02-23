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