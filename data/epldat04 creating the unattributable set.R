### RE-STRUCTURING MESH DATA
rm(list=ls());gc();source(".Rprofile")



# Load RDS file


df <- readRDS(paste0(path_ep_folder,"/working/cleaned/epan03_mesh.RDS"))

# Concatenate DescriptorName for each pmid and change name to MeSH
df_combined <- df %>%
  group_by(pmid) %>%
  summarise(MeSH = paste(DescriptorName, collapse = ", "), .groups = 'drop')

# View new data
View(df_combined)

# Save file -- no need of this!
# saveRDS(df_combined, "epan03_mesh_combined.rds")

### MERGING ALL 3 FILES

# Load RDS files
epan03_abstracts <- readRDS(paste0(path_ep_folder,"/working/cleaned/epan03_abstracts.RDS")) # Contains pmid and abstracts
epan03_titles <- readRDS(paste0(path_ep_folder,"/working/cleaned/epan03_titles.RDS")) # Contains pmid and titles

df_combined <- df_combined %>% distinct(pmid, .keep_all = TRUE)
epan03_titles <- epan03_titles %>% distinct(pmid, .keep_all = TRUE)

# Merge the three data frames on 'pmid'
final_df <- df_combined %>%
  left_join(epan03_abstracts %>% 
              dplyr::select(pmid,abstract), by = "pmid") %>%
  left_join(epan03_titles, by = "pmid") %>% 
  dplyr::filter(year >= 2010) %>% 
  mutate(across(everything(), ~replace(., . %in% c(NA, "NA"), "N/A"))) %>% 
  mutate(pmid = as.numeric(pmid))

### Remove training, dev, and test data duplicates
library(readxl)

# Load the three screened datasets from CSV files
training_screened_df <- read_excel(paste0(path_equity_precision_llm_folder,"/llm training/Methods.xlsx"), sheet = "Training Data")
dev_screened_df <- read_excel(paste0(path_equity_precision_llm_folder,"/llm training/epldat03_Development Data.xlsx"),sheet="Sheet1")
test_screened_df <- read_excel(paste0(path_equity_precision_llm_folder,"/llm training/epldat03_Test Data.xlsx"),sheet="Sheet1")


# Filter out PMIDs that appear in any of the screened datasets
df_filtered <- final_df %>% 
  dplyr::filter(!pmid %in% c(training_screened_df$PMID,
                      dev_screened_df$PMID,
                      test_screened_df$PMID))



# Define file path
write_csv(df_filtered,paste0(path_equity_precision_llm_folder,"/llm training/epldat03_Unattributable Data.csv")  )

