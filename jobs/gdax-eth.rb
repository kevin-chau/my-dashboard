require 'net/http'
require 'json'
require 'uri'

SCHEDULER.every '5s', allow_overlapping: false do


  uri = URI.parse('https://api.coinbase.com/v2/prices/ETH-USD/spot')
  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = true
  request = Net::HTTP::Get.new(uri.request_uri)
  response = http.request(request)
  json_response = JSON.parse(response.body)
  eth_price = json_response['data']['amount']
  eth_price = '%.2f' % eth_price.delete(',').to_f
  #puts btc_price
  send_event('ethprice', { value: eth_price.to_f} )


end
