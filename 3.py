import argparse

def generate_amber_script(start, num):
    script_lines = ["#!/bin/bash\n"]

    for i in range(start, start + num):
        input_rst = f"prod{i}.rst" if i != start else f"prod{i}.rst"
        output_prefix = f"prod{i+1}"

        command = (f"nohup $AMBERHOME/bin/pmemd.cuda -O -i prod_md1.in "
                   f"-p complex_solv.prmtop -c {input_rst} "
                   f"-o {output_prefix}.out -r {output_prefix}.rst -x {output_prefix}.nc")
        script_lines.append(command + "\n")

    script_content = "".join(script_lines)

    with open("./amber.sh", "w") as f:
        f.write(script_content)

    print("amber.sh 生成完毕！")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成 amber.sh 脚本")
    parser.add_argument("-s", type=int, required=True, help="起始段数")
    parser.add_argument("-n", type=int, required=True, help="运行段数")

    args = parser.parse_args()
    generate_amber_script(args.s, args.n)