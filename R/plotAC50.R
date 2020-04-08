#!/usr/bin/env Rscript
library(ggplot2)
library(RColorBrewer)


################
#     MAIN     #
################

args <- commandArgs(TRUE)
pfilin = args[1]
pfilin = "C:/Users/Aborrel/research/NIEHS/BodyMap/data/4245-41-4.csv"


din = read.csv(pfilin, sep = "\t")
din$AC50 = log10(din$AC50)

nb.cols <- 181
mycolors <- colorRampPalette(brewer.pal(8, "Set3"))(nb.cols)

ggplot(din) +
  geom_point(aes(x = AC50, y = Sytem, color = assay_name), size=6)+
  labs(x="", y="")+
  geom_vline(xintercept = 0)+
  scale_fill_manual(values = mycolors)+
  theme(legend.position = "none", axis.text.y = element_text(size = 16), axis.text.x = element_text(size = 16))

ggsave(paste(pfilin, ".png", sep = ""),width = 9, height = 6, dpi = 300)


