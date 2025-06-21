rm(list=ls());gc();source(".Rprofile")



epl05 <- read_csv('preprocessing/epl05_combined_output_Unattributable.csv') %>% 
  separate(combined_category,into = c("pm","dm","ps"),sep = "_") 
epl05_grouped <- read_csv('preprocessing/epl05_combined_output_Unattributable by group.csv') %>% 
  separate(combined_category,into = c("pm","dm","ps"),sep = "_") 

epl06 <- read_csv('preprocessing/epl06_manually screened.csv') %>% 
  separate(combined_category,into = c("pm","dm","ps"),sep = "_") 
epl06_grouped <- read_csv('preprocessing/epl06_manually screened group.csv') %>% 
  separate(combined_category,into = c("pm","dm","ps"),sep = "_") 


epl05_grouped_transposed = bind_rows(epl05_grouped %>% 
                                       dplyr::filter(pm == "yes") %>% 
                                       summarize(across(one_of("European","Non-European"),~sum(.))) ,
                                     epl05_grouped %>% 
                                       dplyr::filter(dm == "yes") %>% 
                                       summarize(across(one_of("European","Non-European"),~sum(.))) ,
                                     epl05_grouped %>% 
                                       dplyr::filter(ps == "yes") %>% 
                                       summarize(across(one_of("European","Non-European"),~sum(.)))) %>% 
  t() %>% data.frame() %>% 
  mutate(r = rownames(.)) %>% 
  rename(
    pm = X1,
    dm = X2,
    ps = X3)


epl05_transposed = bind_rows(epl05 %>% 
                               dplyr::filter(pm == "yes") %>% 
                               summarize(across(Unknown:we,~sum(.))) ,
                             epl05 %>% 
                               dplyr::filter(dm == "yes") %>% 
                               summarize(across(Unknown:we,~sum(.))) ,
                             epl05 %>% 
                               dplyr::filter(ps == "yes") %>% 
                               summarize(across(Unknown:we,~sum(.)))) %>% 
  t() %>% data.frame() %>% 
  mutate(r = rownames(.)) %>% 
  rename(
    pm = X1,
    dm = X2,
    ps = X3)



epl06_grouped_transposed = bind_rows(epl06_grouped %>% 
                               dplyr::filter(pm == "yes") %>% 
                                 summarize(across(one_of("European","Non-European"),~sum(.))) ,
                               epl06_grouped %>% 
                               dplyr::filter(dm == "yes") %>% 
                                 summarize(across(one_of("European","Non-European"),~sum(.))) ,
                               epl06_grouped %>% 
                               dplyr::filter(ps == "yes") %>% 
                               summarize(across(one_of("European","Non-European"),~sum(.)))) %>% 
  t() %>% data.frame() %>% 
  mutate(r = rownames(.)) %>% 
  rename(
    pm = X1,
    dm = X2,
    ps = X3)


epl06_transposed = bind_rows(epl06 %>% 
                               dplyr::filter(pm == "yes") %>% 
                               summarize(across(Unknown:we,~sum(.))) ,
                             epl06 %>% 
                               dplyr::filter(dm == "yes") %>% 
                               summarize(across(Unknown:we,~sum(.))) ,
                             epl06 %>% 
                               dplyr::filter(ps == "yes") %>% 
                               summarize(across(Unknown:we,~sum(.)))) %>% 
  t() %>% data.frame() %>% 
  mutate(r = rownames(.)) %>% 
  rename(
         pm = X1,
         dm = X2,
         ps = X3)

write_csv(epl06_transposed,"paper/table_distribution of studies for manual.csv")
write_csv(epl05_transposed,"paper/table_distribution of studies for unattributable.csv")


write_csv(epl06_grouped_transposed,"paper/table_distribution of studies for manual grouped.csv")
write_csv(epl05_grouped_transposed,"paper/table_distribution of studies for unattributable grouped.csv")
