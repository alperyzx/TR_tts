# TR_tts
Bu proje, Türkçe metinlerdeki gizli vurguları analiz ederek TTS'in (Text-to-Speech) daha doğal ve akıcı bir şekilde konuşmasını sağlar. Böylece dinleyiciyi monotonluktan kurtarır ve daha etkileyici bir deneyim sunar.

📄**givenText.txt**
 TTS'ye iletilecek metin burada belirlenir.

🚀**text2speechLargeText.py**
Uygulamanın ana çalışma dosyası, buradan çalıştırılır.

🔍 **functions.py**
Metindeki vurguları belirleyen temel algoritmalar ve bazı text mining işlemleri burada bulunur.

🎵**combine_mp3.py**
Google TTS API, en fazla 5000 karakterlik metin kabul ettiğinden, dönen küçük ses parçalarını birleştirir.

🎥**create_mp4.py**
 Ses dosyasını bir resimle birleştirerek videoya dönüştürür.
 
🔗 örnek: https://www.youtube.com/playlist?list=PLf1m99shAJb3nJBRfDoBnAJOjKKZbnFwo

youtube kanalıma abone olmayı unutmayın, teşekkürler 😊

# Gereksinimler
<p> <li> pycharm (preferred ide)<br>
<li> python3.13 (additional packages: google-cloud-texttospeech, pydub, mutagen, audioop-lts, moviepy) <br>
<li> ffmpeg (https://github.com/BtbN/FFmpeg-Builds/releases) & add path to system environment <br>
<li> GoogleCloudPlatform https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/texttospeech/snippets <br>
<li> GoogleCloudPlatform auth: https://cloud.google.com/docs/authentication/application-default-credentials </p> 
