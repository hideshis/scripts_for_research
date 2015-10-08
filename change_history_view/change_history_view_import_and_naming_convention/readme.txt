Steps to plot Change History View

1. git clone (pjt_url)
2. cd (pjt_repo)
3. git log --pretty=format:"commit:%H%nauthor:%an%ndate:%at" --name-only > log_(pjt_name).txt
4. mv log_(pjt_name).txt ..
5. cd ..
6. python log_scraper.py (pjt_name)
7. python file_divider.py (pjt_name)
8. cd process(num)
9. git clone (pjt_url)
10. python importing_pc_identifier.py (pjt_name)
11. cd ..
12. repeat steps from 8 to 11 for all process(num) directories
13. python imported_pc_list_formatter.py (pjt_name)
14. python file_id_giver.py (pjt_name)
15. python commit_info_integrator.py (pjt_name)
16. python file_integrator.py (pjt_name)
17. plot Change History View by using ggplot_script.txt