hoge <- read.csv("synthesized_info.csv")
dead <- subset(hoge, status == "dead")
arrive <- subset(hoge, status == "arrive")
par(mfrow=c(2,1))

plot(dead$lifetime, dead$average.bug, xlim = c(0,2500), ylim = c(0,10), xlab = "lifetime [day]" ,ylab = "# of average bug per month", main = "Removed test codes")
abline(v=median(dead$lifetime), lty=2)
plot(arrive$lifetime, arrive$average.bug, xlim = c(0,2500), ylim = c(0,10), xlab = "lifetime [day]" ,ylab = "# of average bug per month", main = "Arriving test codes")
abline(v=median(arrive$lifetime), lty=2)
dev.copy2eps(file="../plot_lifetime_bug.eps")

plot(dead$commit.interval, dead$average.bug, xlim = c(0,950), ylim = c(0,10),  xlab = "commit interval [day]" ,ylab = "# of average bug per month", main = "Removed test codes")
abline(v=median(dead$commit.interval), lty=2)
plot(arrive$commit.interval, arrive$average.bug, xlim = c(0,950), ylim = c(0,10),  xlab = "commit interval [day]" ,ylab = "# of average bug per month", main = "Arriving test codes")
abline(v=median(arrive$commit.interval), lty=2)
dev.copy2eps(file="../plot_interval_bug.eps")

plot(dead$co.evolution.rate, dead$average.bug, xlim = c(0,1), ylim = c(0,10), xlab = "co-evolution rate" ,ylab = "# of average bug per month", main = "Removed test codes")
abline(v=median(dead$co.evolution.rate), lty=2)
plot(arrive$co.evolution.rate, arrive$average.bug, xlim = c(0,1), ylim = c(0,10), xlab = "co-evolution rate" ,ylab = "# of average bug per month", main = "Arriving test codes")
abline(v=median(arrive$co.evolution.rate), lty=2)
dev.copy2eps(file="../plot_co_evo_bug.eps")

> median(dead$lifetime)
[1] 469
> median(arrive$lifetime)
[1] 1289.5
> median(dead$commit.interval)
[1] 28.5
> median(arrive$commit.interval)
[1] 33.75
> median(dead$co.evolution.rate)
[1] 0.1431154
> median(arrive$co.evolution.rate)
[1] 0.05882774
