par(xaxs="i", yaxs="i") 
plot(1, type="n", xlab="% of FEV Mitigated", ylab=NA, xlim=c(0,100), ylim=c(0,100), main="FEV ≈ 10.26Mm^3", xaxt='n', yaxt='n')
axis(side=1, at=c(0,29.2,29.7,29.7,29.7,100), labels = FALSE, tck=-0.01)
text(x=c(0,29.2,29.7,29.7,29.7,100), par("usr")[3]-1, labels=c("0","29.2","","","","100"), srt=45, pos=1, cex=0.8, xpd=TRUE)
axis(side=3, at=c(0,88.9,97.3,98.0,99.3,100), labels = FALSE, tck=-0.01)
text(c(0,88.9,97.3,98.0,99.3,100), par("usr")[3]+106, labels=c("0","","","","",""), srt=45, pos=1, cex=0.8, xpd=TRUE)
arrows(103,0,103,100, xpd = TRUE, length=0.05, code=3)
text(x=105, y=13, label="Worst case", srt=90, pos=1, cex=0.8, xpd=TRUE)
text(x=105, y=96, label="Best case", srt=90, pos=1, cex=0.8, xpd=TRUE)
polygon(x=c(0,29.2,88.9,0), y=c(0,0,100,100), col="tomato1")
polygon(x=c(29.2,29.7,92,70), y=c(0,0,100,100), col="mediumblue")
polygon(x=c(29.7,29.7,95,92), y=c(0,0,100,100), col="yellow")
polygon(x=c(29.7, 29.7, 100, 95), y=c(0, 0, 100, 100), col="purple") 




