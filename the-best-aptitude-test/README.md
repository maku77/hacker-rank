# The Best Aptitude Test

https://www.hackerrank.com/challenges/the-best-aptitude-test/problem?isFullScreen=true

## Run the code

```bash
python main.py < input.txt
```

## Solution / Ideas

与えられた Grade Point Average (GPA) と各科目のスコアの相関係数を求めて、最も相関係数が高い（1.0 に近い）科目を見つければよい。
ピアソンの積率相関係数は以下の式で求められる。

$$
r = \frac{\sum(x_i - \bar{x})(y_i - \bar{y})}{\sqrt{ \sum(x_i - \bar{x})^2 \cdot \sum(y_i - \bar{y})^2}}
$$
