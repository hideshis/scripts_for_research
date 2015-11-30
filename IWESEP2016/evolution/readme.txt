1. git clone (pjt_git_url) target
2. cd target
3. git log --pretty=format:"commit:%H%nauthor:%an%ndate:%at" --name-only > log_target.txt
4. mv log_target.txt ..
5. cd ..
6. python log_scraper.py
7. (remove target git repository)
8. git clone (pjt_url) target
9. python importing_pc_identifier.py
10. python pc_tc_linker.py
11. python commit_info_getter.py
12. python co_evolution_identifier.py
