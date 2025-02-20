rm(list=ls());gc();source(".Rprofile")


epdat03 <- readRDS(paste0(path_ep_folder,"/working/cleaned/epdat03_all abstracts.RDS"))

# eppre02 <- bind_rows(
#   readRDS(paste0(path_ep_folder,"/working/cleaned/eppre02_all abstracts_abstracts part1.RDS")),
#   readRDS(paste0(path_ep_folder,"/working/cleaned/eppre02_all abstracts_abstracts part2.RDS")))

epan03_abstracts <- readRDS(paste0(path_ep_folder,"/working/cleaned/epan03_abstracts.RDS"))


# mesh <- bind_rows(
#   readRDS(paste0(path_ep_folder,"/working/cleaned/eppre02_all abstracts_mesh part1.RDS")),
#   readRDS(paste0(path_ep_folder,"/working/cleaned/eppre02_all abstracts_mesh part2.RDS"))) %>% 
  # group_by(pmid) %>%
  # summarize(MeSH = paste0(DescriptorName,collapse=","))

epan03_mesh <- readRDS(paste0(path_ep_folder,"/working/cleaned/epan03_mesh.RDS")) %>% 
  group_by(pmid) %>%
  summarize(MeSH = paste0(DescriptorName,collapse=","))

development <- read_csv(paste0(path_equity_precision_llm_folder,"/llm training/Original Split CSV without MeSH/Development Data.csv")) %>% 
  left_join(epan03_abstracts %>% 
              dplyr::select(pmid,abstract) %>% 
              rename(epan03_abstract = abstract) %>% 
              mutate(pmid = as.numeric(pmid)),
            by=c("PMID"="pmid")) %>% 
  left_join(epan03_mesh,
            by=c("PMID"="pmid")) %>% 
  mutate(Abstract = case_when(!is.na(abstract) ~ abstract,
                              is.na(abstract) & !is.na(epan03_abstract) ~ epan03_abstract,
                              
                              TRUE ~ ""),
         MeSH = case_when(MeSH == "NA" ~ "",
                          !is.na(MeSH) ~ MeSH,
                          is.na(MeSH) ~ "",
                          TRUE ~ "")) %>% 
  rename('Precision Medicine' = h_precision_medicine,
         'Diabetes' = h_is_diabetes,
         'Source Population' = gbd_region,
         'Correct Source Population' = h_correct_population,
         'Primary Study' = h_primary_study
         ) %>% 
  dplyr::select(PMID,Title,Abstract,MeSH,one_of(c('Source Population','Precision Medicine','Diabetes','Correct Source Population','Primary Study')))


test <- bind_rows(readxl::read_excel(paste0(path_equity_precision_llm_folder,"/llm training/Test Data 1.xlsx")),
                  readxl::read_excel(paste0(path_equity_precision_llm_folder,"/llm training/Test Data 2.xlsx"))) %>% 
  left_join(epan03_abstracts %>% 
              dplyr::select(pmid,abstract) %>% 
              rename(epan03_abstract = abstract) %>% 
              mutate(pmid = as.numeric(pmid)),
            by=c("PMID"="pmid")) %>% 
  left_join(epan03_mesh %>% 
              dplyr::select(pmid,MeSH) %>% 
              rename(epan03_MeSH = MeSH),
            by=c("PMID"="pmid")) %>% 
  mutate(Abstract = case_when(Abstract == "NA" & !is.na(epan03_abstract) ~ epan03_abstract,
                              is.na(Abstract) & !is.na(epan03_abstract) ~ epan03_abstract,
                              !is.na(Abstract) ~ Abstract,
                              TRUE ~ ""),
         MeSH = case_when(MeSH == "NA"& !is.na(epan03_MeSH) ~ epan03_MeSH,
                          is.na(MeSH) & !is.na(epan03_MeSH) ~ epan03_MeSH,
                          !is.na(MeSH) ~ MeSH,
                          is.na(MeSH) ~ "",
                          TRUE ~ "")) %>% 
  dplyr::filter(!is.na(PMID),!is.na(h_precision_medicine)) %>% 
  rename('Precision Medicine' = h_precision_medicine,
         'Diabetes' = h_is_diabetes,
         'Source Population' = gbd_region,
         'Correct Source Population' = h_correct_population,
         'Primary Study' = h_primary_study
  ) %>% 
  dplyr::select(PMID,Title,Abstract,MeSH,one_of(c('Source Population','Precision Medicine','Diabetes','Correct Source Population','Primary Study'))) 


writexl::write_xlsx(development,paste0(path_equity_precision_llm_folder,"/llm training/epldat03_Development Data.xlsx"))
writexl::write_xlsx(test,paste0(path_equity_precision_llm_folder,"/llm training/epldat03_Test Data.xlsx"))

