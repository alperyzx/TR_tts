# TR_tts
Türkçe kelimelerdeki gizli vurguları TTS'in anlamasını sağlar. Böylece dinlerken uyutmaz.  

**givenText.txt**
TTS'e iletilecek metin

**text2speechLargeText.py**
uygulama buradan run edilir.

**functions.py**
vurgu için temel algoritmalar ve bir takım text mining.

**combine_mp3.py**
TTS'ten dönen küçük parçaları birleştir. google TTS api 5000 karaktere kadar kabul ediyor. 

**create_mp4.py**
dilerseniz ses dosyasına bir resim ekleyerek videoya dönüştürün.

örnek: https://www.youtube.com/playlist?list=PLf1m99shAJb3nJBRfDoBnAJOjKKZbnFwo

youtube kanalıma abone olmayı unutmayın, teşekkürler :) 

# Gereksinimler
### python (additional packages)
### pycharm (python ide)
### google cloud 
auth: https://cloud.google.com/docs/authentication/application-default-credentials
