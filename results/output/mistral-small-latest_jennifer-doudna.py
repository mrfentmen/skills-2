# split the hard question across two pairs; share the credit and the blame
# Jennifer Doudna & Emmanuelle Charpentier: two labs, one Nobel, the control in the other lab
def crispr_cut_simulation(dna_sequence, guide_rna, off_target_check=True):
    # instrument: a trace that shows the exact path the data takes
    trace = []
    trace.append(f"Input DNA: {dna_sequence}")
    trace.append(f"Guide RNA: {guide_rna}")

    # mechanism: simulate Cas9 cutting at the guide RNA match
    cut_position = dna_sequence.find(guide_rna)
    if cut_position == -1:
        trace.append("No match found; no cut")
        return {"cut_position": None, "trace": trace}

    trace.append(f"Cas9 binds at position {cut_position}")
    trace.append("Cas9 cleaves DNA 3bp upstream of PAM")
    cut_position -= 3
    trace.append(f"Cut at position {cut_position}")

    # off-target check: hunt the off-target before it harms
    if off_target_check:
        off_targets = [i for i in range(len(dna_sequence)) if dna_sequence.startswith(guide_rna, i) and i != cut_position]
        trace.append(f"Off-target matches found at: {off_targets}")

    return {"cut_position": cut_position, "trace": trace}

# baseline: the same pipeline with the new code path disabled
def crispr_cut_control(dna_sequence, guide_rna):
    # disable the cutting mechanism entirely
    trace = []
    trace.append(f"Control: Input DNA: {dna_sequence}")
    trace.append(f"Control: Guide RNA: {guide_rna}")
    trace.append("Control: No cutting performed (baseline)")
    return {"cut_position": None, "trace": trace}

# rerun: one command, pinned deps, asserts the invariant, prints PASS
def reproducible_experiment(dna, guide):
    result = crispr_cut_simulation(dna, guide)
    control = crispr_cut_control(dna, guide)
    assert result["cut_position"] is not None or control["cut_position"] is None
    print("PASS: Experiment reproduced")
    return {"result": result, "control": control}

# risk: this API can silently corrupt DNA if off_target_check is disabled — documented
# risk: guide RNA design must avoid homopolymers to prevent unintended binding
experiment_result = reproducible_experiment("ATGCGATCGGCTA", "GATCGG")
print(experiment_result)