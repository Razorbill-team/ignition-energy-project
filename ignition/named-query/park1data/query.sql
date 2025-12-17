SELECT t_stamp
    , SUM(inv1_activepower
      +inv2_activepower
      +inv3_activepower
      +inv4_activepower
      +inv5_activepower
      +inv6_activepower
      +inv7_activepower
      +inv8_activepower
      +inv9_activepower
      +inv10_activepower
      +inv11_activepower
      +inv12_activepower
      +inv13_activepower
      +inv14_activepower
      +inv15_activepower
      +inv16_activepower
      +inv17_activepower
      +inv18_activepower
      +inv19_activepower
      +inv20_activepower
      )/1000 as Active_Power
FROM park1_realtimedata
Group by t_stamp
Order by t_stamp DESC