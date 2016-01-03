hoge <- read.csv("synthesized_info.csv")
dead <- subset(hoge, status == "dead")
arrive <- subset(hoge, status == "arrive")
library(ggplot2)
ggplot(data=hoge, aes(x=hoge$lifetime, y=hoge$co.evolution.rate, colour=hoge$status)) + geom_point(aes(size=hoge$average.bug, alpha=.5)) + scale_size_continuous(range = c(2, 10))
