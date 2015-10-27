from yeast_phospho import wd
from pandas import DataFrame, read_csv
from yeast_phospho.utilities import estimate_activity_with_sklearn, regress_out, get_kinases_targets, get_ko_strains

# Import KO steady-state strains
ko_strains = list(get_ko_strains())

# Import growth rates
growth = read_csv('%s/files/strain_relative_growth_rate.txt' % wd, sep='\t', index_col=0)['relative_growth'][ko_strains]

# Import kinase targets
k_targets = get_kinases_targets()


# ---- Estimate kinase activities steady-state
phospho_df = read_csv('%s/tables/pproteomics_steady_state.tab' % wd, sep='\t', index_col=0)[ko_strains]

# Estimate kinase activities
k_activity = DataFrame({c: estimate_activity_with_sklearn(k_targets, phospho_df[c]) for c in phospho_df})
k_activity.to_csv('%s/tables/kinase_activity_steady_state.tab' % wd, sep='\t')

# Regress-out growth
k_activity = DataFrame({k: regress_out(growth[ko_strains], k_activity.ix[k, ko_strains]) for k in k_activity.index}).T
k_activity.to_csv('%s/tables/kinase_activity_steady_state_no_growth.tab' % wd, sep='\t')


# ---- Estimate kinase activities dynamic
# Import phospho FC
phospho_df_dyn = read_csv('%s/tables/pproteomics_dynamic.tab' % wd, sep='\t', index_col=0)

# Estimate kinase activities
k_activity_dyn = DataFrame({c: estimate_activity_with_sklearn(k_targets, phospho_df_dyn[c]) for c in phospho_df_dyn})
k_activity_dyn.to_csv('%s/tables/kinase_activity_dynamic.tab' % wd, sep='\t')