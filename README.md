

# word-predictor

Bir kelimenin ardından hangi kelimelerin gelebileceğini gösteren basit bir **n-gram** modeli.

### Demo

[Link](https://arcane-scrubland-44556.herokuapp.com/) üzerinden uygulamayı test edebilirsiniz.

### Kullanım

Repoyu indirdikten sonra gerekli kütüphaneleri **requirements.txt** ile kurabilirsiniz.

```shell
pip install -r requirements.txt
```

Flask'ın çalışması için komutları girin.

```shell
export FLASK_APP=app.py
flask run
```

Şimdi tarayıcınızda `localhost:5000` ziyaret edin. :tada:

![](./images/img1.png)

### Gerekli Düzenlemeler

- **Kullanıcıdan girdi olarak kelime alınmalı ve en yüksek 3 ihtimalli kelime gösterilmeli. :heavy_check_mark:**
- **Flask ile web üzerinde çalıştırma. :heavy_check_mark:**
- **Kelime Düzeltimi (spell checking)** :heavy_check_mark:
  - **NOT:** Kelime düzeltme kısmında aday kelimeler arasında metindeki frekansı üzerinden bir sıralama yapmak mantıklı olabilir. :warning:
- Kelime kelime ayırım yaparken noktalama işaretleri siliniyor. Ancak nokta'dan sonra gelen kelime ile noktadan önce gelen kelime aslında komşu değildir. Düzeltilmesi gerekiyor. :warning:
  - Öğle yemeğini dışarda yedim. İş yerine yakın yeni bir yer keşfettim.

Bu cümlede **yedim** ile **iş** kelimeleri birbirinden bağımsızdır.
- Daha büyük bir veriseti ile dene.

- Birden fazla kelime ile tahmin yapma. (unigram-trigram ..)


