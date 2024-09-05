from django.db import models

class Average(models.Model):
    code = models.CharField(max_length=6, unique=True)  # 重複のない単一の6桁のコード
    name = models.CharField(max_length=100)  # 野菜の名前（漢字、ひらがな、カタカナ）
    
    # 各月の価格、値がない場合は0にする
    price_01 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_02 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_03 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_04 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_05 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_06 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_07 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_08 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_09 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_10 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_11 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_12 = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} ({self.code})"
