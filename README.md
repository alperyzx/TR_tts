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
<p> <li> python3.13+ (additional packages: pip install -r requirements.txt) <br>
<li> ffmpeg (download latest release: https://github.com/BtbN/FFmpeg-Builds/releases, extract it anywhere and add it's path to system environment <br>
<p> GoogleCloudPlatform Install & Auth: https://cloud.google.com/docs/authentication/application-default-credentials<br> </p>

# Detaylar
<p><li> GoogleCloudPlatform texttospeech https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/texttospeech/snippets  </p>

# Nasıl çalışır
linux:  paketi indir -->  ./run.sh <br>
windows:  paketi indir --> python3.13 app.py