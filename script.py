import os, argparse 

toppath = os.path.abspath(os.getcwd())
pgm = "m4-1.4.19"
srcpath = toppath + "/" + pgm
binpath = srcpath + "/src"
def build_gcov():
    # download the benchmark 
    wget_cmd="wget https://ftp.gnu.org/gnu/m4/m4-1.4.19.tar.gz"
    os.system(wget_cmd)
    
    tar_cmd="tar -xzf m4-1.4.19.tar.gz"
    os.system(tar_cmd)
    
    os.chdir(srcpath)
    os.system('CFLAGS="--coverage -O0 -fprofile-abs-path" LDFLAGS="--coverage" ./configure')
    os.system("make")
    
def run_testcase(file_name):
    with open(file_name, 'r') as f:
        testcases=[l.split('\n')[0] for l in f.readlines()]
    
    os.system("find " + srcpath + ' -name "*.gcda" -exec rm {} \;')
    os.system("find " + srcpath + ' -name "*.gcov" -exec rm {} \;')
    
    os.chdir(binpath)
    print("----------------Run Test-Cases-------------------------------------")
    print("-------------------------------------------------------------------")
    for tc in testcases:
        print(tc)
        os.system(tc)
    gcov_file="cov_result"
    os.system("find " + srcpath + ' -name "*.gcda" -exec gcov -bc {} 1>'+gcov_file+' 2> err \;')
    print("-------------------------------------------------------------------")
    os.system("find " + srcpath + ' -name "*.gcda" -exec rm {} \;')
    os.system("find " + srcpath + ' -name "*.gcov" -exec rm {} \;')
    cal_coverage(gcov_file)

def cal_coverage(cov_file):
    #File 'main.c'
    #Lines executed:18.15% of 639 
    #Branches executed:15.74% of 394 
    #Taken at least once:4.57% of 394 
    #Calls executed:23.73% of 354 
    #Creating 'main.c.gcov'
    coverage=0
    total_coverage=0
    with open(cov_file, 'r') as f:
        lines= f.readlines()
        for line in lines:
            if "Taken at least" in line:
                data=line.split(':')[1]
                percent=float(data.split('% of ')[0])
                total_branches=float((data.split('% of ')[1]).strip())
                covered_branches=int(percent*total_branches/100)
                
                coverage=coverage + covered_branches    
                total_coverage=total_coverage + total_branches 
    print("----------------Results--------------------------------------------")
    print("-------------------------------------------------------------------")
    print("The number of covered branches: " + str(coverage))
    print("The number of total branches: " + str(int(total_coverage)))
    print("-------------------------------------------------------------------")
    return coverage

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--build', action='store_true')
    parser.add_argument("--testcase_file",dest='testcase_file')
    args = parser.parse_args()
    flag = args.build
    testcase_file = args.testcase_file
    
    if flag==True:
        build_gcov()
    else:
        if not testcase_file:
            print("No testcase")
            exit()
        run_testcase(testcase_file)

if __name__ == '__main__':
    main()
