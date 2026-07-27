# Claim 1 method

For each seed 0–24, three independent binary categorical variables are assigned
smooth softmax posteriors. Every one of the 254 nonempty, nonuniversal subsets
of their eight joint assignments is compiled as a disjunction of mutually
exclusive assignment terms; each assignment is a conjunction of independent
atoms. The recursive result is compared with a separately implemented
full-joint probability-and-gradient enumeration. Every seventeenth event is
also checked by central finite differences.

The four primitive rules are checked separately. Three negative controls apply
CI rules to correlated events or constant score mixing to an ME disjunction;
all must be rejected. The verifier exits nonzero on any count, tolerance, or
control failure.
