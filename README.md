# word-predictor
Bir kelimenin ardından hangi kelimelerin gelebileceğini gösteren basit bir **n-gram** modeli.

### Kullanım

Repoyu indirdikten sonra gerekli kütüphaneleri **requirements.txt** ile kurabilirsiniz. Ardından aşağıdaki komutları girin ve [http://localhost:5000](http://localhost:5000/) üzerinde uygulamayı görüntüleyin.

```shell
export FLASK_APP=app.py
flask run
```

![](./images/img1.png)

### Gerekli Düzenlemeler

- Kelime kelime ayırım yaparken noktalama işaretleri siliniyor. Ancak nokta'dan sonra gelen kelime ile noktadan önce gelen kelime aslında komşu değildir. Düzeltilmesi gerekiyor.
    - Öğle yemeğini dışarda yedim. İş yerine yakın yeni bir yer keşfettim.

    Bu cümlede **yedim** ile **İş** kelimeleri birbirinden bağımsızdır.

- Daha büyük bir veriseti ile dene.

- Birden fazla kelime ile tahmin yapma.
- **Kullanıcıdan girdi olarak kelime alınmalı ve en yüksek 3 ihtimalli kelime gösterilmeli. :heavy_check_mark:**
- **Flask ile web üzerinde çalıştırma. :heavy_check_mark:**

