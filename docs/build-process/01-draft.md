
Comecei criando a table via CLI:

```
aws dynamodb create-table \
  --table-name PrinterProfiles \
  --attribute-definitions AttributeName=PrinterId,AttributeType=S \
  --key-schema AttributeName=PrinterId,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
  --region us-east-1
```

Versão oneline para gitbash:

`aws dynamodb create-table --table-name PrinterProfiles --attribute-definitions AttributeName=PrinterId,AttributeType=S --key-schema AttributeName=PrinterId,KeyType=HASH --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 --region us-east-1`

![Table created](../img/01-create-table.png)

Coloquei os itens:

```
aws dynamodb put-item \
  --table-name PrinterProfiles \
  --item '{
    "PrinterId": {"S": "Printer1"},
    "EventCount": {"N": "0"},
    "OutOfBoundsCount": {"N": "0"},
    "Thresholds": {"M": {
      "Lower": {"N": "20"},
      "Upper": {"N": "80"}
    }},
    "Window": {"N": "10"}
  }' \
  --region us-east-1
```

oneline:

`aws dynamodb put-item --table-name PrinterProfiles --item '{"PrinterId":{"S":"Printer1"},"EventCount":{"N":"0"},"OutOfBoundsCount":{"N":"0"},"Thresholds":{"M":{"Lower":{"N":"20"},"Upper":{"N":"80"}}},"Window":{"N":"10"}}' --region us-east-1`

![Printer1 item](../img/02-1st-item.png)

```
aws dynamodb put-item \
  --table-name PrinterProfiles \
  --item '{
    "PrinterId": {"S": "Printer2"},
    "EventCount": {"N": "0"},
    "OutOfBoundsCount": {"N": "0"},
    "Thresholds": {"M": {
      "Lower": {"N": "30"},
      "Upper": {"N": "90"}
    }},
    "Window": {"N": "6"}
  }' \
  --region us-east-1
```

oneline:

`aws dynamodb put-item --table-name PrinterProfiles --item '{"PrinterId":{"S":"Printer2"},"EventCount":{"N":"0"},"OutOfBoundsCount":{"N":"0"},"Thresholds":{"M":{"Lower":{"N":"30"},"Upper":{"N":"90"}}},"Window":{"N":"6"}}' --region us-east-1`

![Printer2 item](../img/03-2nd-item.png)

![Table items list](../img/04-table-items.png)