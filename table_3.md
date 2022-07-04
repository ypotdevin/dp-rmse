| column                    | meaning |
|---------------------------|---------|
| $n$                       | size of the sample |
| $\epsilon$                | privacy budget |
| mean rel. deviation       | the average (over distribution, location, scale and the 10 i.i.d. runs) value of $\frac{\lvert\text{rMSE} - \text{DP rMSE}\rvert}{\text{rMSE}}$ |
| std of the rel. deviation | the standard devition of the above |

|   $n$ |   $\epsilon$ |   mean rel. deviation |   std of the rel. deviation |
|-------|--------------|-----------------------|-----------------------------|
|    10 |         0.01 |            117.46     |                  271.032    |
|    10 |         0.1  |           2083.56     |                40332.1      |
|    10 |         1    |              1.00991  |                    1.82223  |
|    10 |        10    |              0.677315 |                    0.348378 |
|   100 |         0.01 |             31.8797   |                   93.9546   |
|   100 |         0.1  |              1.40967  |                    2.48111  |
|   100 |         1    |              0.780473 |                    0.396785 |
|   100 |        10    |              0.756231 |                    0.333989 |
|  1000 |         0.01 |              5.52861  |                   46.1015   |
|  1000 |         0.1  |              0.885683 |                    2.08742  |
|  1000 |         1    |              0.775388 |                    0.314841 |
|  1000 |        10    |              0.775482 |                    0.314841 |
| 10000 |         0.01 |              0.778711 |                    0.326034 |
| 10000 |         0.1  |              0.775638 |                    0.315425 |
| 10000 |         1    |              0.776331 |                    0.314266 |
| 10000 |        10    |              0.776305 |                    0.314259 |
