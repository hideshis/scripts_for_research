library(ggplot2)
hoge <- read.csv("test.csv")
ggplot(hoge, aes(y=hoge$data, x=hoge$time)) + geom_point()
