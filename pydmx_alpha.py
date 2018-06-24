from ola.ClientWrapper import ClientWrapper

def NewData(data):
  print data

universe = 1

wrapper = ClientWrapper()
client = wrapper.Client()
client.RegisterUniverse(universe, client.REGISTER, NewData)
wrapper.Run()
