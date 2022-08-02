# Trigger Astronomer Dag Docker Action

This action triggers an Astronomer DAG
## Inputs

```yaml
payload:
  description: 'JSON Payload'
  required: false
  default: '{}'
dag_run_id:
  description: 'custom dag run id'
  required: true
  default: ''
webserver_id:
  description: 'webserver id'
  required: true
  default: 'mycompany.astronomer.run/abcd1234'         
dag_name:
  description: 'dag name'
  required: true
  default: ''
username: 
  description: 'username'
  required: true
  default: 'user'     
password: 
  description: 'password'
  required: true
  default: 'password'   
```

## Outputs

## `result`

The result of the DAG

## Example usage

```yaml
uses: explorium-ai/trigger-astronomer-action@v1.0.0
with:
  dag_run_id: random-string
  webserver_id: mycompany.astronomer.run/abcd1234
  dag_name: mydag
  username: myuser
  password: mypassword
  payload: '{"config":"something"}'
```
