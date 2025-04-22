rm(list=ls());gc();source(".Rprofile")

fig_df = readxl::read_excel("preprocessing/dataset for figure 2.xlsx") %>% 
  pivot_longer(cols=-Region,names_to="var",values_to="value")

fig2 <- fig_df %>% 
  ggplot(.,aes(x=Region,y=value,fill=var)) +
  geom_col(position = position_dodge(width=0.9)) +
  theme_bw() +
  xlab("") +
  ylab("") +
  scale_fill_manual(name="",values=c("#F8BDA4",'#77dd77')) +
  theme(legend.position="bottom")
fig2 %>% 
  ggsave(.,filename=paste0(path_equity_precision_llm_folder,"/figures/column plot for disease burden.jpg"),width=8,height = 4)


