import time
import unittest

from SAR.Click_on_hyper_link_in_SAR import Hyperlink
from SAR.arg import arg
from SAR.check_cluster_per_block_csv_download import ClusterPerBlockCsvDownload
from SAR.check_districts_csv_download import DistrictCsvDownload
from SAR.check_dots_on_each_district_block import DotsOnDistrictsBlock
from SAR.check_dots_on_each_districts import DotsOnDistricts
from SAR.check_schools_per_cluster_csv_download import SchoolsPerClusterCsvDownload
from SAR.check_with_total_schools_in_SAR import TotalSchools
from SAR.check_with_total_student_in_SAR import TotalStudents
from SAR.click_on_Home_icon import Home
from SAR.click_on_SAR import DahboardSar
from SAR.click_on_SAR_and_logout import Logout
from SAR.click_on_blocks import Blocks
from SAR.click_on_clusters import Clusters
from SAR.click_on_dashboard import Dashboard
from SAR.click_on_schools import Schools
from SAR.cluster_level_comaparing_dots_with_no_of_schools import ClusterDotsWithNoOfSchools
from SAR.download_blockwise_csv import BlockwiseCsv
from SAR.download_clusterwise_csv import ClusterwiseCsv
from SAR.download_districtwise_csv import DistrictwiseCsv
from SAR.download_schoolwise_csv import SchoolwiseCsv
from reuse_func import GetData


class cQube_Student_Attendance(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.data = GetData()
        self.driver = self.data.get_driver()
        self.data.open_cqube_appln(self.driver)
        self.data.login_cqube(self.driver)
        self.x = arg()
        self.year = self.x.list[0]
        self.month = self.x.list[1]
        self.data.select_month_year(self.year,self.month)

    def test_click_on_dashboard(self):
        self.data.put_log('click on dashboard started')
        dashboard = Dashboard(self.driver)
        dashboard.click_on_dashboard()
        self.data.put_log('click on dashboard ended')

    def test_click_on_student_attendence_report(self):
        self.data.put_log('click on student attendance started')
        sar = DahboardSar(self.driver)
        result = sar.click_on_sar()
        if "Student Attendance Report" in result:
            print("This is Student Attendance Report page")
        else:
            print("SAR page does not exist!...")
        self.data.put_log('click on student attendance ended')

    def test_click_on_blocks(self):
        self.data.put_log('click on blocks started')
        block = Blocks(self.driver)
        result = block.check_markers_on_block_map()
        self.assertNotEqual(0, len(result) - 1, msg="Dots are not present on map")
        self.data.put_log('click on blocks ended')

    def test_click_on_clusters(self):
        self.data.put_log('click on clusters started')
        cluster = Clusters(self.driver)
        result = cluster.check_markers_on_clusters_map()
        self.assertNotEqual(0, len(result) - 1, msg="Dots are not present on map")
        self.data.put_log('click on clusters ended')

    def test_click_on_schools(self):
        self.data.put_log('click on schools started')
        school = Schools(self.driver)
        result = school.check_markers_on_clusters_map()
        self.assertNotEqual(0, int(len(result) - 1), msg="Dots are not present on map")
        self.data.put_log('click on schools ended')

    def test_logout(self):
        self.data.put_log('click on logout started')
        logout = Logout(self.driver)
        result = logout.click_on_logout()
        self.assertEqual("cQube", result, msg="login page is not exist!..")
        self.data.login_cqube(self.driver)
        self.data.select_month_year(self.year, self.month)
        self.data.put_log('click on logout ended')


    def test_check_hyperlinks(self):
        self.data.put_log('click on hyperlinks started')
        hyperlinks = Hyperlink(self.driver)
        result1,result2,choose_dist= hyperlinks.click_on_hyperlinks()
        if result1 == False and result2 == False and choose_dist == "Choose a District " :
            print("hyperlinks are working")
        else :
            raise self.failureException("hyperlinks are not working")
        self.data.put_log('click on hyperlinks ended')

    def test_districtwise_csv_download(self):
        self.data.put_log('district wise downloade started')
        csv = DistrictwiseCsv(self.driver, self.year, self.month)
        result = csv.click_download_icon_of_district()
        if result:
            print("District wise csv report download is working")
            csv.remove_csv()
        else:
            raise self.failureException("District wise csv report download is not working")
        self.data.put_log('district wise downloade ended')

    def test_blockwise_csv_download(self):
        self.data.put_log('block wise csv download started')
        csv = BlockwiseCsv(self.driver, self.year, self.month)
        result = csv.click_download_icon_of_blocks()
        if result:
            print("Block wise csv report download is working")
            csv.remove_csv()
        else:
            raise self.failureException("Block wise csv report download is not working")
        self.data.put_log('block wise csv download ended')

    def test_clusterwise_csv_download(self):
        self.data.put_log('cluster wise csv download started')
        csv = ClusterwiseCsv(self.driver, self.year, self.month)
        result = csv.click_download_icon_of_clusters()
        if result:
            print("Cluster wise csv report download is working")
            csv.remove_csv()
        else:
            raise self.failureException("Cluster wise csv report download is not working")
        self.data.put_log('cluster wise csv download ended')

    def test_schoolwise_cv_download(self):
        self.data.put_log('school wise csv download started')
        csv = SchoolwiseCsv(self.driver, self.year, self.month)
        result = csv.click_download_icon_of_schools()
        if result:
            print("School wise csv report download is working")
            csv.remove_csv()
        else:
            raise self.failureException("School wise csv report download is not working")
        self.data.put_log('school wise csv download ended')

    def test_no_of_schools_is_equals_at_districts_blocks_clusters_schools(self):
        self.data.put_log('Checking Number of schools equals at district,blocks,clusters started')
        tc = TotalSchools(self.driver)
        schools, Bschools = tc.block_no_of_schools()
        self.assertEqual(int(schools), int(Bschools), msg="Block level no of schools are not equal to no of schools ")
        schools, Cschools = tc.cluster_no_of_schools()
        self.assertEqual(int(schools), int(Cschools), msg="Cluster level no of schools are not equal to no of schools ")
        schools, Sschools = tc.schools_no_of_schools()
        self.assertEqual(int(schools), int(Sschools), msg="Cluster level no of schools are not equal to no of schools ")
        self.data.put_log('Checking Number of schools equals at district,blocks,clusters ended')

    def test_total_no_of_students_is_equals_at_districts_blocks_clusters_schools(self):
        self.data.put_log('Checking Number of students equals at district,blocks,clusters started')
        tc = TotalStudents(self.driver)
        student_count, Bstudents = tc.block_total_no_of_students()
        self.assertEqual(int(student_count), int(Bstudents), msg="Block level no of students are not equal")
        student_count, Cstudents = tc.cluster_total_no_of_students()
        self.assertEqual(int(student_count), int(Cstudents), msg="Cluster level no of students are not equal")
        student_count, Sstudents = tc.schools_total_no_of_students()
        self.assertEqual(int(student_count), int(Sstudents), msg="Cluster level no of students are not equal")
        self.data.put_log('Checking Number of students equals at district,blocks,clusters ended')

    def test_no_of_schools_and_no_of_dots_are_equal_at_each_cluster_level(self):
        self.data.put_log('Number of schools and number of dots equals at cluster level started')
        cluster = ClusterDotsWithNoOfSchools(self.driver)
        result = cluster.comapre_cluster()
        if result != 0:
            raise self.failureException('data not matched')
        self.data.put_log('Number of schools and number of dots equals at cluster level ended')

    def test_home_icon(self):
        self.data.put_log('Click on home started')
        home = Home(self.driver)
        home.click_on_blocks_click_on_home_icon()
        result = home.click_HomeButton()
        if "Student Attendance Report" in result:
            print("This is Student Attendance Report page")
        else:
            raise self.failureException('Home Icon is not working')
        self.data.put_log('Click on home ended')

    def test_block_per_district_csv_download(self):
        self.data.put_log('block per district csv download started')
        dist = DistrictCsvDownload(self.driver,self.year,self.month)
        result = dist.check_districts_csv_download()
        if result == 0:
            print("Block per district csv report download is working")
        else:
            raise self.failureException("Block per district csv report download is not working")
        self.data.put_log('block per district csv download ended')

    def test_cluster_per_block_csv_download(self):
        self.data.put_log('cluster per block csv download started')
        block = ClusterPerBlockCsvDownload(self.driver,self.year,self.month)
        result = block.check_csv_download()
        if result == 0:
            print("Cluster per block csv report download is working")
        else:
            raise self.failureException("Cluster per block csv report download is not working")
        self.data.put_log('cluster per block csv download ended')

    def test_schools_per_cluster_csv_download(self):
        self.data.put_log('schools per cluster csv download started')
        schools = SchoolsPerClusterCsvDownload(self.driver,self.year,self.month)
        result = schools.check_csv_download()
        if result == 0:
            print("Schools per cluster csv report download is working")
        else:
            raise self.failureException("Schools per cluster csv report download is working")
        self.data.put_log('schools per cluster csv download ended')

    def test_dots_on_each_districts(self):
        self.data.put_log('checking dots on each started')
        dist = DotsOnDistricts(self.driver)
        result = dist.check_dots_on_each_districts()
        if result != 0:
            raise self.failureException('data not found')
        self.data.put_log('checking dots on each ended')

    def test_dots_on_each_districts_and_each_block(self):
        self.data.put_log('checking dots on each district and blocks started')
        dist_block = DotsOnDistrictsBlock(self.driver)
        result = dist_block.check_dots_on_each_districts_block()
        if result != 0:
            raise self.failureException('data not found')
        self.data.put_log('checking dots on each district and blocks ended')

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
