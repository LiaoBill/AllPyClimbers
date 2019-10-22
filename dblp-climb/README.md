# dblp-climber
## Des
* dblp-ccf-climber
* use config.json to setup and climb paper data.
  * e.g.
  ```
    [Comparative Document Summarisation via Classification.]
    Authors: Umanga Bista, Alexander Patrick Mathews, Minjeong Shin, Aditya Krishna Menon, Lexing Xie
    Doi: https://doi.org/10.1609/aaai.v33i01.330120
    ----------------------------------------
    [ColNet: Embedding the Semantics of Web Tables for Column Type Prediction.]
    Authors: Jiaoyan Chen, Ernesto Jiménez-Ruiz, Ian Horrocks, Charles A. Sutton
    Doi: https://doi.org/10.1609/aaai.v33i01.330129
    ----------------------------------------
    [Improving One-Class Collaborative Filtering via Ranking-Based Implicit Regularizer.]
    Authors: Jin Chen, Defu Lian, Kai Zheng
    Doi: https://doi.org/10.1609/aaai.v33i01.330137
    ----------------------------------------
  ```

## How to use?
> Warning! project currently under development.
* put all dblp link into all_a.md
* use main_brew_all_links.py to fetch all conf/journal links, will be stored in ./dt/ (you will want to create it by yourself)
* run main_process_all_links.py (laziness is causing this step to show up, my bad)
* edit config.json (proxy is not working currently)
  * papaer list is already prepared in order in "./ccf_source_list.md"
* run main_start_paper_search.py to fetch all papers required according to corresponding deep_level
* ENJOY~