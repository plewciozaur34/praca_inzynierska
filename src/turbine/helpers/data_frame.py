class DataFrame:

    def parameters_for_fluent(self, beta, beta_deg, alfa, mach, mach_rel):
        calculated_parameters = pd.DataFrame(
            columns=["beta", "beta_deg", "alfa", "mach", "mach_rel"]
        )
        calculated_parameters = pd.concat(
            [
                calculated_parameters,
                pd.DataFrame(
                    [[beta, beta_deg, alfa, mach, mach_rel]],
                    columns=["beta", "beta_deg", "alfa", "mach", "mach_rel"],
                ),
            ],
            ignore_index=True,
        )
        return calculated_parameters