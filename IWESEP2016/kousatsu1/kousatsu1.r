hoge <- read.csv("synthesized_info.csv")
par(mfrow=c(3,1))
plot(hoge$lifetime, hoge$average.bug, xlab="lifetime [day]", ylab="# of bug per month")
abline(v=869, lty=2)
plot(hoge$commit.interval, hoge$average.bug, xlab="commit interval [day]", ylab="# of bug per month")
abline(v=31, lty=2)
plot(hoge$co.evolution.rate, hoge$average.bug, xlab="co-evolution rate", ylab="# of bug per month")
abline(v=0.100, lty=2)
dev.copy2eps(file="../kousatsu1.eps")