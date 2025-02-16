# TR_tts
Bu proje, Türkçe metinlerdeki gizli vurguları analiz ederek TTS'in (Text-to-Speech) daha doğal ve akıcı bir şekilde konuşmasını sağlar. Böylece dinleyiciyi monotonluktan kurtarır ve daha etkileyici bir deneyim sunar.

📄**givenText.txt**
TTS'e iletilecek metin

🚀**text2speechLargeText.py**
uygulama buradan run edilir.

🔍 **functions.py**
vurgu için temel algoritmalar ve bir takım text mining.

🎵**combine_mp3.py**
TTS'ten dönen küçük parçaları birleştir. google TTS api 5000 karaktere kadar kabul ediyor. 

🎥**create_mp4.py**
dilerseniz ses dosyasına bir resim ekleyerek videoya dönüştürün.

🔗 örnek: https://www.youtube.com/playlist?list=PLf1m99shAJb3nJBRfDoBnAJOjKKZbnFwo

youtube kanalıma abone olmayı unutmayın, teşekkürler 😊

# Gereksinimler
<p> <li> pycharm (preferred ide)<br>
<li> python3.13 (additional packages: google-cloud-texttospeech, pydub, mutagen, audioop-lts, moviepy) <br>
<li> ffmpeg (https://github.com/BtbN/FFmpeg-Builds/releases) & add path to system environment <br>
<li> GoogleCloudPlatform https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/texttospeech/snippets <br>
<li> GoogleCloudPlatform auth: https://cloud.google.com/docs/authentication/application-default-credentials </p> 
