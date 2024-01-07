import subprocess

def handler(event, context):
  print(event)
  #bucket = event['Records'][0]['s3']['bucket']['name']
  #print(bucket)
  #key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
  #print(key)
  subprocess.check_call(["bash","dbscript.sh"])
  print("Hello")