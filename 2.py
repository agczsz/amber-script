import argparse

def generate_amber_script(n):
    script_content = """# Step 1: Minimization
nohup $AMBERHOME/bin/pmemd.cuda -O -i step1min.in -o step1min.out -p complex_solv.prmtop -c complex_solv.inpcrd -ref complex_solv.inpcrd -r step1min.rst

# Step 2: Minimization
nohup $AMBERHOME/bin/pmemd.cuda -O -i step2min.in -o step2min.out -p complex_solv.prmtop -c step1min.rst -ref step1min.rst -r step2min.rst

# Step 3: Minimization
nohup $AMBERHOME/bin/pmemd.cuda -O -i step3min.in -o step3min.out -p complex_solv.prmtop -c step2min.rst -ref step2min.rst -r step3min.rst

# Step 4: Minimization
nohup $AMBERHOME/bin/pmemd.cuda -O -i step4min.in -o step4min.out -p complex_solv.prmtop -c step3min.rst -ref step3min.rst -r step4min.rst

# Step 5: Heating
nohup $AMBERHOME/bin/pmemd.cuda -O -i step2heat.in -o step2heat.out -p complex_solv.prmtop -c step4min.rst -ref step4min.rst -r step2heat.rst

# Step 6: Heating
nohup $AMBERHOME/bin/pmemd.cuda -O -i step3heat.in -o step3heat.out -p complex_solv.prmtop -c step2heat.rst -ref step2heat.rst -r step3heat.rst

# Step 7: Heating
nohup $AMBERHOME/bin/pmemd.cuda -O -i step4heat.in -o step4heat.out -p complex_solv.prmtop -c step3heat.rst -ref step3heat.rst -r step4heat.rst

# Step 8: Heating
nohup $AMBERHOME/bin/pmemd.cuda -O -i step5heat.in -o step5heat.out -p complex_solv.prmtop -c step4heat.rst -ref step4heat.rst -r step5heat.rst

# Step 9: Heating
nohup $AMBERHOME/bin/pmemd.cuda -O -i step6heat.in -o step6heat.out -p complex_solv.prmtop -c step5heat.rst -ref step5heat.rst -r step6heat.rst

# Step 10: Heating
nohup $AMBERHOME/bin/pmemd.cuda -O -i step7heat.in -o step7heat.out -p complex_solv.prmtop -c step6heat.rst -ref step6heat.rst -r step7heat.rst

# Step 11: Heating
nohup $AMBERHOME/bin/pmemd.cuda -O -i step8heat.in -o step8heat.out -p complex_solv.prmtop -c step7heat.rst -ref step7heat.rst -r step8heat.rst

# Step 12: Heating
nohup $AMBERHOME/bin/pmemd.cuda -O -i step9heat.in -o step9heat.out -p complex_solv.prmtop -c step8heat.rst -ref step8heat.rst -r step9heat.rst

# Step 13: Heating
nohup $AMBERHOME/bin/pmemd.cuda -O -i step10heat.in -o step10heat.out -p complex_solv.prmtop -c step9heat.rst -ref step9heat.rst -r step10heat.rst

# Step 14: Heating
nohup $AMBERHOME/bin/pmemd.cuda -O -i step11heat.in -o step11heat.out -p complex_solv.prmtop -c step10heat.rst -ref step10heat.rst -r step11heat.rst

# Step 15: Equilibration
nohup $AMBERHOME/bin/pmemd.cuda -O -i step12equ.in -o step12equ.out -p complex_solv.prmtop -c step11heat.rst -ref step11heat.rst -r step12equ.rst

# Step 16: Equilibration
nohup $AMBERHOME/bin/pmemd.cuda -O -i step13equ.in -o step13equ.out -p complex_solv.prmtop -c step12equ.rst -ref step12equ.rst -r step13equ.rst

# Step 17: Equilibration
nohup $AMBERHOME/bin/pmemd.cuda -O -i step14equ.in -o step14equ.out -p complex_solv.prmtop -c step13equ.rst -ref step13equ.rst -r step14equ.rst

# Step 18: Equilibration
nohup $AMBERHOME/bin/pmemd.cuda -O -i step14equ.in -o step15equ.out -p complex_solv.prmtop -c step14equ.rst -ref step14equ.rst -r step15equ.rst
"""

    # Add production run steps based on -n argument
    for i in range(1, n + 1):
        prev_rst = "step15equ.rst" if i == 1 else f"prod{i - 1}.rst"
        script_content += f"nohup $AMBERHOME/bin/pmemd.cuda -O -i prod_md1.in -p complex_solv.prmtop -c {prev_rst} -o prod{i}.out -r prod{i}.rst -x prod{i}.nc\n"
    
    # Write to file
    with open("amber.sh", "w") as f:
        f.write(script_content)
    print("amber.sh has been generated successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate AMBER simulation script")
    parser.add_argument("-n", type=int, required=True, help="Number of production runs")
    args = parser.parse_args()
    generate_amber_script(args.n)
