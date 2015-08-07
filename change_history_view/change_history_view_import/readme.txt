Steps to plot Change History View

1. git clone (pjt_url)
2. git log --pretty=format:"commit:%H%nauthor:%an%ndate:%at" --name-only > log_(pjt_name).txt
3. python log_scraper.py (pjt_name)
4. python file_divider.py (pjt_name)
5. cd process(num)
6. git clone (pjt_url)
7. python importing_pc_identifier.py (pjt_name)
8. cd ..
9. repeat steps from 5 to 8 for all process(num) directories
10. python imported_pc_list_formatter.py (pjt_name)
11. python file_id_giver.py (pjt_name)
12. python commit_info_integrator.py (pjt_name)
13. python file_integrator.py (pjt_name)
14. plot Change History View by using ggplot_script.txt