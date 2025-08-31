for b in (DS0726, PS1029):
    b.setPricingEngine(engine)
    print("===", b.maturityDate(), "===")
    print("Clean:", b.cleanPrice())
    print("Dirty:", b.dirtyPrice())
    print("Accrued:", b.accruedAmount())
    # YTM (roczna kapitalizacja)
    clean_price = ql.SimpleQuote(b.cleanPrice())
    ytm = ql.BondFunctions.yield_(b, 
                                 ql.QuoteHandle(clean_price),
                                 ACTACT_ICMA, 
                                 ql.Compounded, 
                                 ql.Annual)
    print("YTM:", ytm)
    dur_mod = ql.BondFunctions.duration(
        b, ytm, ACTACT_ICMA, ql.Compounded, ql.Annual, ql.Duration.Modified)
    print("ModDuration:", dur_mod)
    dv01 = dur_mod * b.dirtyPrice() / 100.0
    print("DV01:", dv01)
    print("Convexity:", ql.BondFunctions.convexity(
        b, ytm, ACTACT_ICMA, ql.Compounded, ql.Annual))
