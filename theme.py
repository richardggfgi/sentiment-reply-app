"""หน้าตาแอป: ธีมเดียวกับสไลด์ (พื้นน้ำเงิน ดาว เมฆ การ์ดม่วงอ่อนไล่ฟ้าขอบเข้ม)"""
import html

import streamlit as st

_BG = {'lines': "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 900' preserveAspectRatio='xMidYMid slice'%3E%3Cg fill='none' stroke='%235a8aff' stroke-width='16' stroke-linejoin='round' opacity='.6'%3E%3Cpath d='M864.9 520.0 L866.7 523.4 L868.1 526.9 L868.8 530.5 L869.0 534.1 L868.6 537.7 L867.5 541.2 L865.9 544.6 L863.7 547.8 L861.0 550.8 L857.9 553.7 L854.5 556.3 L850.8 558.7 L846.8 560.9 L842.8 563.0 L838.7 564.8 L834.6 566.5 L830.5 568.1 L826.5 569.6 L822.5 571.1 L818.7 572.5 L814.9 573.9 L811.1 575.3 L807.4 576.7 L803.8 578.1 L800.0 579.4 L796.3 580.7 L792.5 581.9 L788.6 583.0 L784.7 583.9 L780.7 584.8 L776.6 585.4 L772.5 585.9 L768.3 586.2 L764.2 586.3 L760.0 586.3 L755.8 586.1 L751.7 585.7 L747.6 585.3 L743.5 584.8 L739.5 584.2 L735.4 583.6 L731.4 583.0 L727.2 582.3 L723.1 581.7 L718.8 581.1 L714.5 580.4 L710.0 579.8 L705.5 579.0 L700.9 578.1 L696.2 577.1 L691.5 576.0 L686.9 574.6 L682.4 573.0 L678.1 571.1 L674.0 569.0 L670.3 566.5 L667.0 563.8 L664.2 560.9 L661.9 557.7 L660.1 554.4 L659.0 550.8 L658.4 547.2 L658.4 543.6 L658.9 539.9 L659.8 536.3 L661.2 532.8 L662.9 529.4 L664.8 526.1 L666.8 523.0 L668.9 520.0 L670.9 517.1 L672.9 514.4 L674.6 511.7 L676.2 509.1 L677.5 506.6 L678.6 504.0 L679.5 501.3 L680.2 498.6 L680.8 495.8 L681.4 492.9 L681.9 490.0 L682.5 486.9 L683.3 483.8 L684.2 480.7 L685.4 477.5 L687.0 474.4 L688.8 471.4 L691.0 468.5 L693.6 465.7 L696.5 463.1 L699.7 460.7 L703.2 458.5 L706.9 456.5 L710.9 454.8 L715.0 453.3 L719.3 451.9 L723.6 450.8 L728.1 449.8 L732.6 449.0 L737.1 448.3 L741.6 447.7 L746.2 447.2 L750.8 446.8 L755.4 446.5 L760.0 446.3 L764.6 446.2 L769.3 446.3 L773.9 446.6 L778.5 447.0 L783.1 447.7 L787.6 448.6 L791.9 449.8 L796.1 451.3 L800.1 453.0 L803.9 455.0 L807.3 457.2 L810.5 459.6 L813.5 462.2 L816.1 464.9 L818.4 467.7 L820.5 470.5 L822.4 473.4 L824.1 476.2 L825.7 479.0 L827.3 481.7 L828.9 484.2 L830.6 486.7 L832.4 489.1 L834.5 491.4 L836.7 493.6 L839.2 495.8 L841.9 498.0 L844.8 500.3 L847.8 502.7 L850.9 505.2 L854.1 507.8 L857.1 510.6 L860.0 513.6 L862.6 516.7Z'/%3E%3Cpath d='M966.2 520.0 L968.8 526.7 L970.4 533.5 L970.8 540.4 L970.0 547.2 L968.1 553.9 L965.0 560.4 L960.9 566.6 L955.9 572.5 L950.1 578.0 L943.7 583.2 L936.8 588.0 L929.6 592.4 L922.1 596.4 L914.6 600.2 L907.0 603.8 L899.6 607.1 L892.3 610.3 L885.1 613.4 L878.0 616.5 L871.1 619.5 L864.3 622.5 L857.5 625.5 L850.7 628.4 L843.8 631.2 L836.8 633.9 L829.7 636.5 L822.4 638.8 L815.0 640.9 L807.4 642.6 L799.7 644.1 L791.8 645.2 L783.9 646.0 L775.9 646.5 L768.0 646.6 L760.0 646.4 L752.1 646.1 L744.2 645.5 L736.3 644.8 L728.5 644.1 L720.6 643.3 L712.7 642.5 L704.7 641.7 L696.5 640.8 L688.2 640.0 L679.7 639.2 L670.9 638.2 L662.0 637.1 L653.0 635.8 L643.9 634.2 L634.8 632.2 L625.8 629.7 L617.0 626.8 L608.6 623.4 L600.8 619.4 L593.6 614.8 L587.2 609.7 L581.7 604.1 L577.3 598.0 L573.9 591.5 L571.6 584.8 L570.3 577.9 L570.2 570.9 L570.9 563.9 L572.5 557.0 L574.8 550.2 L577.7 543.6 L580.9 537.3 L584.3 531.3 L587.7 525.5 L591.0 520.0 L594.0 514.7 L596.7 509.5 L599.0 504.4 L600.9 499.4 L602.3 494.3 L603.3 489.1 L604.1 483.8 L604.6 478.4 L605.1 472.7 L605.7 466.9 L606.4 461.0 L607.5 454.9 L609.0 448.8 L611.0 442.7 L613.7 436.7 L617.0 430.8 L621.1 425.1 L625.8 419.7 L631.2 414.7 L637.2 410.0 L643.7 405.7 L650.8 401.8 L658.2 398.3 L666.0 395.2 L674.0 392.5 L682.2 390.0 L690.6 387.9 L699.0 386.0 L707.6 384.3 L716.2 382.8 L724.8 381.5 L733.5 380.4 L742.3 379.5 L751.1 378.9 L760.0 378.4 L768.9 378.3 L777.8 378.6 L786.7 379.3 L795.5 380.4 L804.1 382.0 L812.5 384.1 L820.6 386.8 L828.3 389.9 L835.6 393.6 L842.5 397.7 L848.7 402.2 L854.5 407.0 L859.7 412.1 L864.4 417.3 L868.7 422.6 L872.6 427.9 L876.3 433.1 L879.8 438.2 L883.3 443.0 L886.9 447.7 L890.7 452.1 L894.9 456.4 L899.3 460.5 L904.3 464.6 L909.6 468.5 L915.3 472.6 L921.4 476.7 L927.8 481.1 L934.2 485.7 L940.6 490.6 L946.8 495.8 L952.7 501.4 L958.0 507.3 L962.5 513.5Z'/%3E%3Cpath d='M1070.6 520.0 L1073.0 530.0 L1073.7 540.2 L1072.6 550.2 L1069.8 560.2 L1065.4 569.8 L1059.5 579.0 L1052.4 587.9 L1044.1 596.2 L1034.9 603.9 L1025.1 611.2 L1014.9 618.0 L1004.4 624.3 L993.8 630.2 L983.2 635.8 L972.7 641.2 L962.5 646.4 L952.4 651.4 L942.6 656.4 L932.9 661.3 L923.2 666.2 L913.6 671.0 L903.9 675.8 L894.1 680.3 L884.1 684.7 L873.8 688.8 L863.3 692.6 L852.4 695.9 L841.4 698.9 L830.1 701.3 L818.6 703.3 L806.9 704.7 L795.2 705.7 L783.5 706.2 L771.7 706.4 L760.0 706.3 L748.3 705.9 L736.6 705.4 L725.0 704.8 L713.2 704.2 L701.4 703.5 L689.3 702.9 L677.1 702.3 L664.5 701.7 L651.7 701.0 L638.6 700.1 L625.2 699.0 L611.5 697.5 L597.8 695.5 L584.1 692.9 L570.7 689.6 L557.6 685.5 L545.0 680.6 L533.3 674.8 L522.6 668.1 L513.1 660.6 L504.9 652.4 L498.3 643.4 L493.1 633.9 L489.6 623.9 L487.6 613.7 L487.1 603.3 L487.9 592.9 L489.9 582.7 L492.8 572.7 L496.4 563.0 L500.4 553.7 L504.6 544.7 L508.8 536.1 L512.7 527.9 L516.2 520.0 L519.2 512.3 L521.5 504.7 L523.2 497.1 L524.3 489.5 L524.9 481.7 L525.1 473.7 L525.1 465.5 L525.0 457.0 L525.2 448.3 L525.6 439.4 L526.7 430.3 L528.4 421.2 L531.1 412.1 L534.7 403.1 L539.3 394.3 L545.0 385.8 L551.7 377.8 L559.5 370.2 L568.1 363.1 L577.6 356.6 L587.8 350.7 L598.5 345.3 L609.8 340.4 L621.4 336.0 L633.3 332.0 L645.4 328.4 L657.6 325.2 L670.0 322.3 L682.6 319.6 L695.2 317.2 L707.9 315.1 L720.8 313.3 L733.8 311.8 L746.8 310.8 L760.0 310.3 L773.2 310.3 L786.3 311.0 L799.4 312.4 L812.2 314.5 L824.7 317.5 L836.8 321.2 L848.4 325.7 L859.3 330.9 L869.6 336.9 L879.1 343.3 L887.9 350.3 L895.9 357.5 L903.2 365.0 L910.0 372.5 L916.3 380.0 L922.3 387.3 L928.2 394.4 L934.0 401.1 L940.1 407.6 L946.5 413.7 L953.5 419.6 L961.0 425.3 L969.1 430.8 L977.8 436.3 L987.1 441.9 L996.9 447.7 L1007.0 453.8 L1017.1 460.3 L1027.2 467.3 L1036.9 474.9 L1045.9 482.9 L1054.0 491.6 L1061.0 500.7 L1066.6 510.2Z'/%3E%3Cpath d='M1175.9 520.0 L1176.8 533.4 L1175.5 546.7 L1172.0 559.9 L1166.3 572.7 L1158.8 585.0 L1149.6 596.8 L1139.1 608.0 L1127.5 618.5 L1115.1 628.4 L1102.2 637.7 L1089.0 646.5 L1075.7 654.7 L1062.6 662.7 L1049.6 670.3 L1036.8 677.7 L1024.3 684.9 L1012.0 692.1 L999.9 699.2 L987.8 706.2 L975.6 713.1 L963.3 719.9 L950.8 726.4 L937.9 732.7 L924.7 738.6 L911.0 743.9 L896.9 748.8 L882.4 753.0 L867.7 756.7 L852.6 759.6 L837.3 761.9 L821.9 763.7 L806.4 764.9 L790.9 765.6 L775.5 766.0 L760.0 766.2 L744.5 766.1 L729.0 766.1 L713.4 766.0 L697.5 765.9 L681.4 765.9 L665.0 765.9 L648.2 765.9 L630.9 765.7 L613.3 765.2 L595.2 764.4 L577.0 763.0 L558.6 760.8 L540.2 757.8 L522.2 753.8 L504.6 748.7 L487.9 742.4 L472.3 734.9 L458.1 726.2 L445.4 716.3 L434.5 705.4 L425.6 693.6 L418.6 680.9 L413.7 667.8 L410.8 654.2 L409.8 640.5 L410.3 626.8 L412.3 613.2 L415.4 600.0 L419.3 587.2 L423.6 574.8 L428.1 563.0 L432.5 551.7 L436.4 540.8 L439.7 530.3 L442.3 520.0 L444.0 509.9 L444.9 499.7 L445.0 489.5 L444.5 479.1 L443.6 468.4 L442.5 457.4 L441.4 446.1 L440.7 434.4 L440.5 422.5 L441.2 410.4 L443.0 398.2 L446.0 386.0 L450.3 374.0 L456.1 362.3 L463.3 351.0 L471.9 340.2 L481.8 330.0 L492.9 320.5 L505.1 311.6 L518.2 303.5 L532.1 296.0 L546.6 289.1 L561.6 282.9 L577.0 277.1 L592.7 271.8 L608.6 267.0 L624.7 262.5 L641.0 258.3 L657.4 254.5 L674.1 251.1 L690.9 248.1 L708.0 245.6 L725.2 243.7 L742.6 242.5 L760.0 242.2 L777.4 242.7 L794.8 244.2 L811.8 246.7 L828.5 250.4 L844.7 255.1 L860.1 260.8 L874.9 267.5 L888.7 275.1 L901.6 283.4 L913.5 292.3 L924.6 301.5 L934.8 311.0 L944.3 320.5 L953.4 329.9 L962.0 339.0 L970.6 347.8 L979.3 356.2 L988.3 364.1 L997.9 371.6 L1008.1 378.7 L1019.1 385.6 L1030.9 392.3 L1043.5 399.0 L1056.8 405.9 L1070.7 413.1 L1084.9 420.8 L1099.1 429.1 L1113.1 438.1 L1126.5 447.8 L1138.9 458.2 L1149.9 469.5 L1159.4 481.4 L1167.0 493.8 L1172.6 506.8Z'/%3E%3Cpath d='M1279.3 520.0 L1277.8 536.6 L1273.6 553.0 L1266.9 569.0 L1257.9 584.5 L1247.0 599.4 L1234.5 613.5 L1220.8 626.9 L1206.1 639.6 L1191.0 651.6 L1175.6 662.9 L1160.1 673.8 L1144.8 684.2 L1129.7 694.3 L1114.9 704.2 L1100.3 713.9 L1086.0 723.4 L1071.8 732.9 L1057.6 742.3 L1043.2 751.6 L1028.6 760.6 L1013.6 769.3 L998.0 777.6 L982.0 785.4 L965.3 792.5 L948.1 799.0 L930.4 804.8 L912.2 809.7 L893.7 813.9 L874.9 817.3 L855.9 820.0 L836.8 822.1 L817.6 823.7 L798.4 825.0 L779.2 826.0 L760.0 826.8 L740.7 827.6 L721.1 828.5 L701.3 829.4 L681.1 830.4 L660.5 831.4 L639.3 832.3 L617.6 833.0 L595.4 833.3 L572.7 833.0 L549.7 831.9 L526.5 829.9 L503.5 826.7 L480.8 822.1 L458.9 816.0 L438.0 808.4 L418.4 799.2 L400.6 788.5 L384.7 776.3 L371.1 762.7 L359.8 748.0 L350.9 732.3 L344.5 715.9 L340.5 699.0 L338.6 682.0 L338.6 664.9 L340.3 648.1 L343.1 631.8 L346.8 615.9 L350.9 600.6 L355.1 586.0 L358.9 572.0 L362.2 558.5 L364.6 545.4 L366.1 532.6 L366.5 520.0 L365.9 507.4 L364.5 494.6 L362.3 481.5 L359.8 468.1 L357.1 454.3 L354.6 440.1 L352.6 425.5 L351.6 410.5 L351.6 395.3 L353.2 380.1 L356.3 364.8 L361.2 349.8 L367.9 335.1 L376.4 320.9 L386.7 307.3 L398.6 294.5 L412.0 282.4 L426.8 271.1 L442.7 260.6 L459.5 250.8 L477.0 241.8 L495.2 233.4 L513.8 225.7 L532.8 218.4 L552.1 211.6 L571.7 205.2 L591.5 199.3 L611.6 193.8 L632.0 188.8 L652.7 184.4 L673.8 180.6 L695.1 177.6 L716.6 175.6 L738.3 174.6 L760.0 174.8 L781.6 176.3 L803.0 179.1 L823.8 183.3 L844.1 188.9 L863.6 195.8 L882.2 203.8 L899.7 212.9 L916.1 222.9 L931.5 233.5 L945.7 244.5 L959.1 255.7 L971.7 266.9 L983.7 277.9 L995.4 288.6 L1007.1 298.7 L1019.0 308.2 L1031.4 317.2 L1044.5 325.7 L1058.5 333.7 L1073.4 341.5 L1089.4 349.0 L1106.3 356.7 L1124.1 364.6 L1142.4 373.0 L1161.0 382.0 L1179.6 391.9 L1197.7 402.7 L1214.9 414.4 L1230.8 427.2 L1245.0 440.9 L1257.1 455.6 L1266.7 471.0 L1273.7 487.0 L1278.0 503.4Z'/%3E%3Cpath d='M1378.6 520.0 L1373.9 539.7 L1366.3 559.0 L1356.1 577.7 L1343.7 595.7 L1329.6 612.9 L1314.1 629.2 L1297.7 644.8 L1280.7 659.6 L1263.6 673.7 L1246.4 687.3 L1229.4 700.4 L1212.7 713.2 L1196.3 725.7 L1180.2 738.1 L1164.2 750.3 L1148.4 762.4 L1132.4 774.3 L1116.1 786.0 L1099.4 797.5 L1082.1 808.5 L1064.2 819.0 L1045.5 828.9 L1026.0 838.0 L1005.8 846.3 L985.0 853.7 L963.6 860.2 L941.7 865.7 L919.4 870.4 L896.9 874.4 L874.3 877.7 L851.6 880.4 L828.8 882.8 L806.0 885.0 L783.1 887.1 L760.0 889.3 L736.6 891.5 L712.9 893.8 L688.7 896.2 L663.8 898.5 L638.3 900.7 L612.2 902.6 L585.3 904.0 L558.0 904.5 L530.2 904.0 L502.3 902.3 L474.5 898.9 L447.2 893.9 L420.8 887.0 L395.7 878.2 L372.2 867.3 L350.8 854.6 L331.7 840.0 L315.2 823.8 L301.4 806.2 L290.5 787.4 L282.4 767.8 L277.0 747.7 L274.0 727.4 L273.2 707.1 L274.0 687.2 L276.2 667.7 L279.1 648.9 L282.5 630.8 L285.7 613.5 L288.4 596.9 L290.3 580.9 L291.2 565.4 L290.8 550.2 L289.3 535.1 L286.6 520.0 L283.0 504.7 L278.7 489.1 L274.0 473.0 L269.3 456.4 L265.0 439.3 L261.5 421.7 L259.2 403.8 L258.4 385.5 L259.4 367.2 L262.5 348.9 L267.8 330.8 L275.2 313.1 L284.9 296.0 L296.7 279.6 L310.5 263.9 L326.0 249.2 L343.1 235.3 L361.5 222.3 L380.9 210.1 L401.3 198.7 L422.3 188.0 L443.9 177.9 L465.9 168.4 L488.4 159.4 L511.2 150.9 L534.4 142.9 L558.0 135.5 L582.0 128.6 L606.4 122.5 L631.3 117.2 L656.6 113.0 L682.2 109.9 L708.1 108.2 L734.1 107.9 L760.0 109.3 L785.6 112.2 L810.8 116.9 L835.2 123.2 L858.8 131.1 L881.3 140.3 L902.7 150.7 L922.8 162.2 L941.7 174.3 L959.4 186.8 L976.1 199.5 L992.0 212.1 L1007.3 224.3 L1022.4 236.0 L1037.6 247.1 L1053.1 257.5 L1069.2 267.2 L1086.3 276.2 L1104.5 284.8 L1123.8 293.0 L1144.3 301.1 L1165.9 309.4 L1188.4 318.0 L1211.5 327.3 L1234.8 337.5 L1257.9 348.7 L1280.3 361.1 L1301.5 374.8 L1321.0 389.8 L1338.3 406.0 L1353.0 423.3 L1364.7 441.6 L1373.3 460.7 L1378.4 480.2 L1380.2 500.1Z'/%3E%3Cpath d='M1472.1 520.0 L1463.8 542.6 L1452.7 564.5 L1439.2 585.7 L1423.8 606.0 L1407.0 625.5 L1389.3 644.0 L1371.0 661.8 L1352.6 678.8 L1334.2 695.3 L1316.0 711.3 L1298.2 726.9 L1280.7 742.2 L1263.5 757.4 L1246.4 772.4 L1229.2 787.3 L1211.8 801.9 L1193.9 816.3 L1175.4 830.3 L1156.1 843.8 L1135.9 856.7 L1114.8 868.8 L1092.7 880.0 L1069.7 890.2 L1045.9 899.5 L1021.3 907.6 L996.2 914.8 L970.7 921.0 L944.9 926.4 L918.9 931.2 L892.8 935.4 L866.5 939.4 L840.2 943.1 L813.8 946.8 L787.1 950.7 L760.0 954.6 L732.4 958.7 L704.2 962.9 L675.2 967.0 L645.5 970.9 L614.8 974.3 L583.4 977.0 L551.4 978.6 L518.9 978.9 L486.2 977.5 L453.7 974.3 L421.8 968.9 L391.0 961.2 L361.6 951.1 L334.2 938.6 L309.1 923.9 L286.7 907.0 L267.3 888.1 L251.0 867.6 L237.9 845.8 L227.9 823.1 L220.8 799.8 L216.4 776.3 L214.3 752.9 L213.9 729.9 L214.8 707.5 L216.5 685.9 L218.4 665.2 L220.0 645.3 L221.0 626.3 L220.9 607.9 L219.5 590.1 L216.8 572.6 L212.6 555.2 L207.3 537.7 L200.9 520.0 L193.9 501.8 L186.6 483.1 L179.5 463.8 L173.0 443.9 L167.7 423.4 L163.9 402.5 L162.0 381.2 L162.4 359.8 L165.3 338.4 L170.7 317.3 L178.8 296.6 L189.5 276.5 L202.6 257.2 L218.0 238.7 L235.3 221.1 L254.5 204.5 L275.1 188.8 L296.9 174.0 L319.7 160.1 L343.3 146.8 L367.6 134.2 L392.4 122.2 L417.7 110.8 L443.5 99.9 L469.8 89.5 L496.6 79.9 L524.0 70.9 L552.1 62.9 L580.7 55.9 L609.9 50.2 L639.6 46.0 L669.6 43.3 L699.8 42.5 L730.0 43.6 L760.0 46.6 L789.4 51.6 L818.1 58.5 L845.9 67.2 L872.4 77.5 L897.7 89.1 L921.6 101.7 L944.2 115.0 L965.6 128.8 L985.8 142.6 L1005.3 156.2 L1024.2 169.3 L1043.0 181.7 L1061.9 193.3 L1081.4 204.0 L1101.7 214.0 L1123.1 223.2 L1145.7 231.8 L1169.8 240.1 L1195.2 248.4 L1221.7 257.0 L1249.2 266.1 L1277.3 276.1 L1305.5 287.2 L1333.3 299.6 L1360.1 313.6 L1385.4 329.1 L1408.5 346.1 L1429.0 364.7 L1446.4 384.7 L1460.2 405.8 L1470.3 427.9 L1476.5 450.7 L1478.7 473.8 L1477.2 497.0Z'/%3E%3Cpath d='M1558.8 520.0 L1547.0 545.2 L1532.8 569.7 L1516.5 593.2 L1498.9 615.8 L1480.3 637.4 L1461.3 658.2 L1442.1 678.3 L1423.1 697.8 L1404.4 716.7 L1386.0 735.3 L1367.9 753.6 L1350.0 771.8 L1332.1 789.7 L1314.0 807.5 L1295.5 825.0 L1276.3 842.2 L1256.2 858.9 L1235.2 875.0 L1213.0 890.3 L1189.6 904.8 L1165.0 918.2 L1139.4 930.5 L1112.7 941.7 L1085.3 951.8 L1057.1 960.7 L1028.5 968.7 L999.5 975.9 L970.3 982.4 L941.0 988.5 L911.5 994.3 L881.9 999.9 L852.1 1005.7 L821.9 1011.6 L791.3 1017.7 L760.0 1024.0 L727.9 1030.3 L694.9 1036.5 L660.9 1042.4 L626.0 1047.6 L590.0 1051.9 L553.4 1054.8 L516.2 1056.0 L478.8 1055.2 L441.6 1052.1 L405.1 1046.4 L369.8 1037.9 L336.2 1026.7 L304.8 1012.6 L276.0 995.8 L250.3 976.6 L227.8 955.1 L208.8 931.8 L193.3 907.0 L181.1 881.3 L172.1 854.9 L165.9 828.3 L162.1 801.9 L160.0 776.0 L159.2 750.9 L159.0 726.7 L158.9 703.5 L158.3 681.3 L156.8 660.0 L154.1 639.4 L149.8 619.5 L144.0 599.8 L136.8 580.3 L128.2 560.6 L118.6 540.6 L108.4 520.0 L98.1 498.8 L88.2 476.8 L79.3 454.1 L71.8 430.8 L66.3 406.9 L63.2 382.6 L62.7 358.2 L65.2 333.7 L70.7 309.5 L79.2 285.8 L90.6 262.7 L104.9 240.4 L121.6 219.0 L140.6 198.5 L161.5 179.1 L184.0 160.6 L207.9 143.0 L232.8 126.2 L258.7 110.1 L285.3 94.8 L312.5 80.1 L340.4 65.9 L368.8 52.4 L398.0 39.5 L427.8 27.3 L458.5 16.1 L489.9 6.0 L522.2 -2.9 L555.1 -10.2 L588.8 -15.8 L623.0 -19.4 L657.4 -20.9 L691.9 -20.2 L726.2 -17.3 L760.0 -12.0 L793.0 -4.7 L824.9 4.7 L855.6 15.8 L884.9 28.3 L912.8 41.8 L939.2 56.1 L964.4 70.7 L988.4 85.3 L1011.6 99.5 L1034.4 113.0 L1057.1 125.6 L1080.1 137.3 L1103.8 148.0 L1128.5 157.7 L1154.6 166.6 L1182.1 174.9 L1211.1 183.0 L1241.6 191.1 L1273.4 199.6 L1306.1 208.9 L1339.3 219.4 L1372.5 231.2 L1405.1 244.7 L1436.4 260.0 L1465.8 277.2 L1492.6 296.3 L1516.2 317.3 L1536.2 339.8 L1552.2 363.8 L1563.9 388.9 L1571.1 414.9 L1574.0 441.2 L1572.7 467.8 L1567.5 494.1Z'/%3E%3Cpath d='M1638.5 520.0 L1623.9 547.7 L1607.3 574.5 L1589.3 600.2 L1570.5 625.1 L1551.2 649.0 L1531.9 672.2 L1512.8 694.7 L1494.0 716.8 L1475.5 738.4 L1457.3 759.9 L1439.2 781.1 L1420.9 802.1 L1402.3 822.8 L1383.0 843.3 L1362.8 863.4 L1341.5 882.9 L1318.9 901.7 L1294.9 919.6 L1269.4 936.5 L1242.6 952.3 L1214.5 966.8 L1185.3 980.2 L1155.1 992.3 L1124.1 1003.3 L1092.6 1013.3 L1060.7 1022.5 L1028.5 1031.1 L996.2 1039.3 L963.7 1047.3 L931.0 1055.3 L898.1 1063.4 L864.6 1071.8 L830.6 1080.4 L795.8 1089.2 L760.0 1098.1 L723.1 1106.7 L685.0 1114.9 L645.8 1122.2 L605.5 1128.3 L564.2 1132.7 L522.4 1135.0 L480.3 1134.8 L438.5 1131.9 L397.4 1125.9 L357.7 1116.7 L319.8 1104.3 L284.4 1088.6 L251.9 1069.8 L222.7 1048.3 L197.0 1024.2 L175.1 998.2 L157.0 970.5 L142.4 941.8 L131.2 912.4 L122.8 883.0 L116.8 853.8 L112.6 825.3 L109.5 797.6 L106.9 771.0 L104.1 745.6 L100.7 721.3 L96.1 698.0 L90.0 675.5 L82.3 653.6 L72.9 632.0 L61.9 610.5 L49.6 588.7 L36.3 566.5 L22.5 543.7 L8.9 520.0 L-4.1 495.5 L-15.7 470.1 L-25.5 444.0 L-32.9 417.2 L-37.5 390.0 L-39.0 362.5 L-37.1 335.0 L-31.7 307.8 L-23.0 281.0 L-10.9 254.8 L4.1 229.5 L22.0 205.0 L42.3 181.6 L64.6 159.1 L88.7 137.6 L114.3 117.0 L141.0 97.3 L168.7 78.3 L197.3 59.9 L226.6 42.2 L256.6 25.1 L287.5 8.7 L319.2 -6.9 L351.9 -21.7 L385.5 -35.4 L420.2 -47.8 L455.9 -58.7 L492.6 -67.8 L530.2 -74.8 L568.4 -79.5 L607.1 -81.9 L645.9 -81.7 L684.5 -78.9 L722.7 -73.6 L760.0 -65.9 L796.2 -56.1 L831.1 -44.4 L864.5 -31.3 L896.4 -17.0 L926.8 -2.1 L955.9 12.9 L983.9 27.8 L1011.1 42.1 L1037.9 55.6 L1064.7 68.0 L1092.0 79.3 L1120.2 89.4 L1149.6 98.4 L1180.5 106.6 L1213.1 114.2 L1247.3 121.6 L1283.1 129.2 L1320.3 137.4 L1358.4 146.6 L1396.9 157.2 L1435.2 169.6 L1472.6 184.0 L1508.4 200.6 L1541.9 219.5 L1572.3 240.6 L1599.1 263.8 L1621.8 289.0 L1639.9 315.8 L1653.2 343.9 L1661.6 373.0 L1665.3 402.7 L1664.4 432.5 L1659.3 462.2 L1650.5 491.4Z'/%3E%3Cpath d='M1712.0 520.0 L1695.6 550.0 L1677.9 579.0 L1659.3 607.0 L1640.4 634.1 L1621.5 660.5 L1602.9 686.2 L1584.5 711.4 L1566.5 736.2 L1548.6 760.8 L1530.7 785.1 L1512.5 809.3 L1493.7 833.1 L1474.0 856.6 L1453.1 879.7 L1430.7 902.1 L1406.8 923.6 L1381.2 944.2 L1353.9 963.7 L1325.0 981.9 L1294.7 998.9 L1263.0 1014.5 L1230.3 1028.9 L1196.8 1042.2 L1162.6 1054.4 L1128.1 1065.9 L1093.2 1076.9 L1058.2 1087.6 L1023.0 1098.1 L987.5 1108.8 L951.6 1119.8 L915.2 1131.0 L878.1 1142.5 L839.9 1154.2 L800.6 1165.9 L760.0 1177.3 L718.0 1188.0 L674.6 1197.7 L630.0 1205.7 L584.3 1211.7 L537.8 1215.2 L491.2 1215.8 L444.7 1213.1 L399.1 1206.9 L354.9 1197.0 L312.8 1183.3 L273.3 1166.0 L237.0 1145.3 L204.2 1121.5 L175.2 1094.9 L150.3 1066.1 L129.2 1035.7 L111.9 1004.2 L98.1 972.1 L87.1 939.9 L78.5 908.2 L71.6 877.2 L65.7 847.4 L60.1 818.7 L54.1 791.3 L47.2 765.2 L38.9 740.1 L29.0 716.0 L17.2 692.4 L3.6 669.1 L-11.6 645.8 L-28.1 622.2 L-45.5 597.9 L-63.2 572.9 L-80.5 547.0 L-96.8 520.0 L-111.4 492.0 L-123.7 463.2 L-133.1 433.6 L-139.3 403.4 L-141.9 373.0 L-140.8 342.4 L-135.7 312.1 L-127.0 282.2 L-114.6 253.0 L-98.9 224.5 L-80.3 197.0 L-59.1 170.5 L-35.6 144.9 L-10.3 120.2 L16.5 96.5 L44.6 73.6 L73.8 51.4 L103.9 29.8 L134.9 9.0 L166.9 -11.2 L199.8 -30.7 L233.8 -49.4 L269.0 -66.9 L305.5 -83.3 L343.3 -98.1 L382.3 -111.1 L422.6 -122.0 L464.0 -130.6 L506.3 -136.6 L549.2 -139.8 L592.3 -140.2 L635.3 -137.8 L677.8 -132.5 L719.5 -124.8 L760.0 -114.7 L799.1 -102.7 L836.8 -89.1 L872.8 -74.6 L907.2 -59.5 L940.3 -44.4 L972.4 -29.6 L1003.7 -15.6 L1034.6 -2.7 L1065.8 9.0 L1097.6 19.3 L1130.4 28.3 L1164.7 36.2 L1200.6 43.2 L1238.4 49.6 L1278.0 56.0 L1319.3 62.7 L1361.9 70.3 L1405.5 79.2 L1449.3 89.9 L1492.7 102.6 L1535.0 117.8 L1575.3 135.6 L1612.8 156.0 L1646.9 179.1 L1676.9 204.6 L1702.2 232.4 L1722.5 262.0 L1737.5 293.1 L1747.3 325.4 L1751.9 358.3 L1751.6 391.5 L1746.9 424.5 L1738.4 457.1 L1726.5 489.0Z'/%3E%3Cpath d='M1781.1 520.0 L1764.1 552.2 L1746.4 583.4 L1728.4 613.7 L1710.6 643.2 L1692.9 672.1 L1675.6 700.5 L1658.5 728.5 L1641.5 756.3 L1624.3 783.9 L1606.5 811.2 L1587.8 838.2 L1567.9 864.8 L1546.5 890.8 L1523.4 916.2 L1498.4 940.6 L1471.4 964.0 L1442.5 986.1 L1411.8 1006.9 L1379.4 1026.4 L1345.6 1044.5 L1310.7 1061.4 L1274.9 1077.1 L1238.4 1091.9 L1201.5 1106.0 L1164.3 1119.7 L1126.9 1133.1 L1089.3 1146.7 L1051.3 1160.4 L1012.9 1174.5 L973.7 1188.9 L933.7 1203.7 L892.5 1218.7 L849.9 1233.5 L805.8 1247.9 L760.0 1261.4 L712.6 1273.5 L663.8 1283.7 L613.7 1291.4 L562.8 1296.2 L511.5 1297.5 L460.5 1295.1 L410.4 1288.7 L361.7 1278.0 L315.3 1263.2 L271.7 1244.3 L231.4 1221.6 L195.0 1195.5 L162.5 1166.5 L134.3 1135.2 L110.1 1102.1 L89.7 1068.0 L72.9 1033.3 L58.9 998.8 L47.3 964.8 L37.2 931.7 L27.9 899.9 L18.7 869.5 L8.9 840.5 L-2.0 812.9 L-14.5 786.4 L-28.9 760.8 L-45.2 735.9 L-63.5 711.1 L-83.4 686.3 L-104.5 660.9 L-126.3 634.9 L-148.2 607.9 L-169.4 579.7 L-189.2 550.4 L-206.9 520.0 L-221.9 488.5 L-233.6 456.1 L-241.6 423.1 L-245.5 389.7 L-245.2 356.1 L-240.7 322.7 L-232.2 289.7 L-219.7 257.4 L-203.8 225.8 L-184.7 195.1 L-162.8 165.3 L-138.7 136.5 L-112.6 108.6 L-84.9 81.5 L-55.9 55.3 L-25.7 29.7 L5.6 4.8 L38.0 -19.4 L71.4 -42.9 L106.1 -65.7 L142.2 -87.4 L179.7 -108.0 L218.7 -127.1 L259.4 -144.4 L301.7 -159.7 L345.6 -172.6 L390.7 -182.8 L437.0 -190.1 L484.0 -194.4 L531.4 -195.5 L578.7 -193.5 L625.6 -188.5 L671.7 -180.8 L716.6 -170.7 L760.0 -158.6 L801.8 -145.1 L842.0 -130.6 L880.6 -115.8 L917.8 -101.0 L953.9 -86.9 L989.4 -73.7 L1024.7 -61.8 L1060.3 -51.5 L1096.6 -42.6 L1134.3 -35.1 L1173.5 -28.9 L1214.6 -23.5 L1257.7 -18.6 L1302.8 -13.6 L1349.6 -8.1 L1397.7 -1.4 L1446.7 7.0 L1495.8 17.5 L1544.4 30.5 L1591.4 46.4 L1636.2 65.3 L1677.8 87.3 L1715.5 112.2 L1748.6 140.0 L1776.6 170.3 L1799.1 202.8 L1816.0 236.9 L1827.2 272.3 L1833.0 308.5 L1833.7 345.0 L1829.7 381.3 L1821.8 417.3 L1810.6 452.5 L1796.8 486.7Z'/%3E%3Cpath d='M1847.6 520.0 L1831.4 554.4 L1815.0 587.8 L1798.7 620.5 L1782.7 652.6 L1766.9 684.2 L1751.3 715.4 L1735.5 746.4 L1719.3 777.2 L1702.3 807.7 L1684.1 837.9 L1664.3 867.6 L1642.7 896.7 L1619.1 925.1 L1593.2 952.4 L1565.1 978.6 L1534.8 1003.5 L1502.5 1027.1 L1468.3 1049.2 L1432.7 1070.0 L1395.8 1089.5 L1358.0 1107.9 L1319.6 1125.5 L1280.7 1142.5 L1241.5 1159.2 L1202.1 1175.8 L1162.4 1192.5 L1122.4 1209.7 L1081.7 1227.3 L1040.2 1245.3 L997.6 1263.6 L953.6 1282.1 L908.0 1300.4 L860.5 1318.0 L811.2 1334.4 L760.0 1349.2 L707.1 1361.6 L652.8 1371.1 L597.4 1377.2 L541.7 1379.4 L486.1 1377.2 L431.4 1370.5 L378.3 1359.1 L327.5 1343.1 L279.7 1322.6 L235.4 1298.1 L195.1 1269.8 L159.0 1238.5 L127.2 1204.8 L99.5 1169.3 L75.8 1132.8 L55.6 1095.9 L38.2 1059.2 L23.0 1023.3 L9.3 988.5 L-3.9 955.1 L-17.2 923.3 L-31.3 893.1 L-46.8 864.3 L-64.1 836.8 L-83.4 810.1 L-104.8 784.0 L-128.1 758.1 L-153.0 731.9 L-179.1 705.1 L-205.6 677.4 L-232.0 648.6 L-257.3 618.4 L-280.8 586.9 L-301.8 554.1 L-319.6 520.0 L-333.7 484.9 L-343.5 449.1 L-348.9 412.7 L-349.7 376.2 L-346.0 339.7 L-337.8 303.6 L-325.6 268.0 L-309.7 233.2 L-290.5 199.3 L-268.5 166.2 L-244.1 134.1 L-217.7 102.8 L-189.6 72.3 L-160.1 42.5 L-129.3 13.4 L-97.3 -15.0 L-64.0 -42.7 L-29.3 -69.7 L6.8 -95.8 L44.6 -120.8 L84.2 -144.4 L125.7 -166.4 L169.1 -186.4 L214.6 -204.0 L261.8 -218.9 L310.7 -230.9 L360.9 -239.6 L412.0 -245.0 L463.7 -246.9 L515.4 -245.6 L566.7 -241.0 L617.1 -233.6 L666.3 -223.8 L714.0 -212.0 L760.0 -198.8 L804.3 -184.8 L847.0 -170.6 L888.3 -156.8 L928.6 -143.7 L968.3 -132.0 L1007.9 -121.7 L1048.0 -113.1 L1089.0 -106.2 L1131.5 -100.8 L1175.7 -96.6 L1222.1 -93.3 L1270.5 -90.3 L1321.1 -87.1 L1373.4 -83.0 L1427.1 -77.5 L1481.5 -69.9 L1535.9 -59.7 L1589.5 -46.5 L1641.3 -30.0 L1690.5 -10.0 L1736.1 13.4 L1777.4 40.3 L1813.6 70.3 L1844.4 103.2 L1869.2 138.5 L1888.0 175.6 L1900.9 214.2 L1908.1 253.5 L1910.0 293.3 L1907.2 333.0 L1900.4 372.2 L1890.3 410.6 L1877.7 448.1 L1863.2 484.6Z'/%3E%3C/g%3E%3C/svg%3E", 'cl': "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 560 300'%3E%3Cdefs%3E%3ClinearGradient id='c' x1='0' y1='0' x2='0' y2='1'%3E%3Cstop offset='0' stop-color='%23e6f8ff'/%3E%3Cstop offset='1' stop-color='%238fd2ff'/%3E%3C/linearGradient%3E%3ClinearGradient id='d' x1='0' y1='0' x2='0' y2='1'%3E%3Cstop offset='0' stop-color='%23b9e6ff'/%3E%3Cstop offset='1' stop-color='%236fb9ff'/%3E%3C/linearGradient%3E%3C/defs%3E%3Cpath d='M0 300 L0 150 A55.0 55 0 0 1 110 150 A45.0 40 0 0 1 200 150 A60.0 60 0 0 1 320 150 A50.0 30 0 0 1 420 150 A50 150 0 0 1 470 300Z' fill='url%28%23d%29' opacity='.8'/%3E%3Cpath d='M0 300 L0 210 A45.0 45 0 0 1 90 210 A60.0 70 0 0 1 210 210 A50.0 40 0 0 1 310 210 A65.0 55 0 0 1 440 210 A30.0 20 0 0 1 500 210 A50 90 0 0 1 550 300Z' fill='url%28%23c%29'/%3E%3C/svg%3E", 'cr': "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 560 320'%3E%3Cdefs%3E%3ClinearGradient id='c' x1='0' y1='0' x2='0' y2='1'%3E%3Cstop offset='0' stop-color='%23e6f8ff'/%3E%3Cstop offset='1' stop-color='%238fd2ff'/%3E%3C/linearGradient%3E%3ClinearGradient id='d' x1='0' y1='0' x2='0' y2='1'%3E%3Cstop offset='0' stop-color='%23b9e6ff'/%3E%3Cstop offset='1' stop-color='%236fb9ff'/%3E%3C/linearGradient%3E%3C/defs%3E%3Cpath d='M90 320 A50 170 0 0 1 140 150 A50.0 45 0 0 1 240 150 A60.0 65 0 0 1 360 150 A50.0 40 0 0 1 460 150 A50.0 50 0 0 1 560 150 A50 170 0 0 1 610 320Z' fill='url%28%23d%29' opacity='.8'/%3E%3Cpath d='M10 320 A50 90 0 0 1 60 230 A30.0 20 0 0 1 120 230 A55.0 45 0 0 1 230 230 A65.0 80 0 0 1 360 230 A50.0 50 0 0 1 460 230 A60.0 70 0 0 1 580 230 A50 90 0 0 1 630 320Z' fill='url%28%23c%29'/%3E%3C/svg%3E", 'ct': "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 420 150'%3E%3Cdefs%3E%3ClinearGradient id='c' x1='0' y1='0' x2='0' y2='1'%3E%3Cstop offset='0' stop-color='%23e6f8ff'/%3E%3Cstop offset='1' stop-color='%238fd2ff'/%3E%3C/linearGradient%3E%3ClinearGradient id='d' x1='0' y1='0' x2='0' y2='1'%3E%3Cstop offset='0' stop-color='%23b9e6ff'/%3E%3Cstop offset='1' stop-color='%236fb9ff'/%3E%3C/linearGradient%3E%3C/defs%3E%3Cpath d='M0 0 L0 60 A45.0 25 0 0 0 90 60 A55.0 40 0 0 0 200 60 A60.0 30 0 0 0 320 60 A50.0 35 0 0 0 420 60 L420 0Z' fill='url%28%23c%29' opacity='.75'/%3E%3C/svg%3E", 'star': "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='%23f6d99a' stroke='%232a2f66' stroke-width='.9' stroke-linejoin='round' d='M12 2l2.9 6.3 6.9.8-5.1 4.7 1.4 6.8L12 17.1 5.9 20.6l1.4-6.8L2.2 9.1l6.9-.8z'/%3E%3C/svg%3E"}

CSS = """
<style>
:root {
  --ground: #3f73ff; --ink: #1a1e4a; --ink-soft: #3b4180; --line: #2a2f66; --sun: #ffd84d;
  --card-top: #f3f0ff; --card-mid: #dde8ff; --card-bot: #9cc5ff;
  --good: #14804f; --good-bg: #d8f5e5; --bad: #b8243e; --bad-bg: #ffe0e5; --mid: #4a5170; --mid-bg: #e6e9f5;
}
/* พื้นหลังแบบสไลด์: เส้นคลื่นวงซ้อน เมฆ และดาว (SVG ฝังในไฟล์) */
.stApp { background: var(--ground) !important; }
[data-testid="stMain"] {
  background:
    url("__STAR__") 2.5% 34% / 46px no-repeat,
    url("__STAR__") 97.5% 20% / 40px no-repeat,
    url("__STAR__") 96.5% 64% / 32px no-repeat,
    url("__STAR__") 3.5% 70% / 28px no-repeat,
    url("__CL__") left bottom / min(420px, 60%) auto no-repeat,
    url("__CR__") right bottom / min(460px, 65%) auto no-repeat,
    url("__CT__") right top / min(340px, 50%) auto no-repeat,
    url("__LINES__") center / cover no-repeat,
    var(--ground) !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stMain"] .block-container { padding-top: 2.2rem; max-width: 1180px; }

/* หัวเรื่อง */
.fx-hero { text-align: center; margin: 0 0 1.2rem; }
.stMarkdown .fx-kicker, .fx-kicker { font-family: Kanit, sans-serif; font-weight: 700; font-size: clamp(28px, 4.5vw, 42px) !important; line-height: 1 !important;
  color: var(--sun); text-shadow: 2px 2px 0 var(--line); letter-spacing: .5px; margin: 0; }
.stMarkdown .fx-title, .fx-title { font-family: Kanit, sans-serif; font-weight: 600; font-size: clamp(22px, 3.6vw, 36px) !important; line-height: 1.25 !important;
  color: #fff; margin: .35rem 0 .25rem; text-wrap: balance; text-shadow: 0 2px 0 rgba(26,30,74,.25); }
.stMarkdown .fx-sub, .fx-sub { color: #dbe6ff; font-size: 15px !important; margin: 0; }
.fx-sub b { color: #fff; font-family: Kanit, sans-serif; font-weight: 600; letter-spacing: .4px; }

/* แท็บเป็นปุ่มเม็ดยา */
[data-testid="stMain"] .stTabs [role="tablist"] { gap: 8px; justify-content: center; flex-wrap: wrap;
  background: transparent !important; border: 0 !important; box-shadow: none !important; margin-bottom: 14px; overflow: visible; }
[data-testid="stMain"] .stTabs [role="tablist"] > :not([role="tab"]) { display: none !important; }
[data-testid="stMain"] .stTabs > div:first-child { border: 0 !important; box-shadow: none !important; }
.stTabs [role="tablist"]::after, .stTabs [role="tablist"]::before { content: none !important; display: none !important;
  height: 0 !important; background: transparent !important; }
[data-testid="stMain"] [data-testid="stTab"] { height: auto !important; padding: 8px 22px !important; border-radius: 999px;
  border: 2px solid var(--line) !important; background: rgba(255,255,255,.18); margin: 0 0 4px !important; }
[data-testid="stMain"] [data-testid="stTab"] p { color: #fff !important; font-family: Kanit, sans-serif; font-weight: 500; font-size: 17px !important; }
[data-testid="stMain"] [data-testid="stTab"][aria-selected="true"] { background: var(--sun); box-shadow: 0 3px 0 var(--line) !important; }
.stTabs .react-aria-SelectionIndicator, .stTabs [class*="SelectionIndicator"] { display: none !important; }
[data-testid="stMain"] [data-testid="stTab"][aria-selected="true"] p { color: var(--ink) !important; }
[data-testid="stMain"] [data-testid="stTab"]:focus-visible { outline: 3px solid var(--sun); outline-offset: 2px; }

/* เนื้อหาแต่ละแท็บอยู่ในการ์ดใหญ่ ขอบสองชั้น */
[data-testid="stMain"] [data-testid="stTabPanel"] {
  position: relative; padding: 26px 26px 22px !important; border: 2px solid var(--line); border-radius: 28px;
  background: linear-gradient(180deg, var(--card-top) 0%, var(--card-mid) 70%, var(--card-bot) 160%);
}
[data-testid="stMain"] [data-testid="stTabPanel"]::before { content: ""; position: absolute; inset: 6px;
  border: 1.5px solid var(--line); border-radius: 22px; opacity: .6; pointer-events: none; }
@media (max-width: 640px) { [data-testid="stMain"] [data-testid="stTabPanel"] { padding: 18px 14px !important; } }

/* การ์ดรีวิว (container มีขอบ) */
[data-testid="stMain"] [data-testid="stVerticalBlock"][class*="st-key-card"],
[data-testid="stMain"] .stTabs [data-testid="stVerticalBlockBorderWrapper"] {
  background: rgba(255,255,255,.72); border: 2px solid var(--line) !important; border-radius: 22px;
}
.fx-rev-head { display: flex; flex-wrap: wrap; gap: 6px 10px; align-items: center; margin-bottom: 2px; }
.fx-id { font-family: Kanit, sans-serif; font-weight: 600; font-size: 17px !important; color: var(--ink); }
.fx-stars { color: #c98a00; letter-spacing: 2px; font-size: 14px; }
.fx-pill { font-family: Kanit, sans-serif; font-weight: 600; font-size: 13px; border-radius: 999px; padding: 1px 11px;
  border: 1.5px solid currentColor; white-space: nowrap; line-height: 1.6; }
.fx-pos { color: var(--good); background: var(--good-bg); }
.fx-neg { color: var(--bad); background: var(--bad-bg); }
.fx-neu { color: var(--mid); background: var(--mid-bg); }
.fx-high { color: var(--ink); background: var(--sun); border-color: var(--line); }
.fx-medium { color: #8a5a00; background: #fff1c9; }
.fx-asp { color: var(--ink-soft); background: rgba(255,255,255,.7); font-weight: 500; }
.fx-said { background: #fff; border: 1.5px solid var(--line); border-radius: 14px; padding: 10px 14px; margin: 6px 0 4px;
  color: var(--ink); }
.fx-status { font-family: Kanit, sans-serif; font-weight: 500; padding-top: .45rem; color: var(--ink-soft); }
.fx-status.ok { color: var(--good); }

/* ปุ่ม: ขอบเข้ม เงาแบบสไลด์ ปุ่มหลักสีเหลือง */
[data-testid="stMain"] .stButton button, [data-testid="stMain"] .stDownloadButton button {
  border: 2px solid var(--line); box-shadow: 0 3px 0 var(--line); font-family: Kanit, sans-serif; font-weight: 500;
  background: #fff; color: var(--ink);
}
[data-testid="stMain"] .stButton button[kind="primary"], [data-testid="stSidebar"] .stButton button[kind="primary"] {
  background: var(--sun); color: var(--ink); border: 2px solid var(--line);
}
[data-testid="stMain"] .stButton button:active { transform: translateY(2px); box-shadow: 0 1px 0 var(--line); }

/* ตัวเลขสรุป */
[data-testid="stMain"] [data-testid="stMetric"] { background: rgba(255,255,255,.75); border: 2px solid var(--line);
  border-radius: 20px; padding: 12px 16px; }
[data-testid="stMain"] [data-testid="stMetricValue"] { font-family: Kanit, sans-serif; font-weight: 700; }

/* แถบซ้าย */
[data-testid="stSidebar"] { border-right: 2px solid var(--line); }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { font-family: Kanit, sans-serif; }


/* แท็บเกี่ยวกับระบบ */
.fx-sec { font-family: Kanit, sans-serif; font-weight: 600; font-size: 22px !important; color: var(--ink); margin: 0 0 10px; }
.fx-flow { display: flex; flex-wrap: nowrap; align-items: stretch; gap: 6px; margin-bottom: 24px; }
.fx-step { flex: 1 1 0; min-width: 0; background: #fff; border: 2px solid var(--line); border-radius: 18px; padding: 10px 14px; }
.fx-step b { display: block; font-family: Kanit, sans-serif; font-weight: 600; font-size: 16px; color: var(--ink); }
.fx-step span { font-size: 13.5px; color: var(--ink-soft); }
.fx-step.hl { background: var(--sun); }
.fx-arrow { align-self: center; font-family: Kanit, sans-serif; font-size: 22px; color: var(--line); }
.fx-grid { display: grid; gap: 12px; grid-template-columns: repeat(auto-fit, minmax(min(100%, 220px), 1fr)); margin-bottom: 24px; }
.fx-stat { background: #fff; border: 2px solid var(--line); border-radius: 18px; padding: 12px 16px; }
.fx-stat .v { font-family: Kanit, sans-serif; font-weight: 700; font-size: 34px; line-height: 1.1; color: var(--ink); font-variant-numeric: tabular-nums; }
.fx-stat .l { font-family: Kanit, sans-serif; font-weight: 500; font-size: 15px; color: var(--ink); margin-top: 2px; }
.fx-stat .d { font-size: 13px; color: var(--ink-soft); margin-top: 4px; }
.fx-note { font-size: 13px; color: var(--ink-soft); margin: 0; }
@media (max-width: 760px) { .fx-flow { display: grid; grid-template-columns: 1fr 1fr; } .fx-arrow { display: none; } .fx-step:last-child { grid-column: 1 / -1; } }

/* กราฟแดชบอร์ด (HTML) */
.fx-chart { background: #fff; border: 2px solid var(--line); border-radius: 20px; padding: 16px 18px; height: 100%; }
.fx-chart h4 { font-family: Kanit, sans-serif; font-weight: 600; font-size: 19px !important; color: var(--ink); margin: 0 0 12px; padding: 0; }
.fx-stack { display: flex; height: 30px; border: 2px solid var(--line); border-radius: 999px; overflow: hidden; background: #f3f0ff; }
.fx-stack span { display: block; height: 100%; }
.fx-legend { display: grid; gap: 8px; margin-top: 14px; }
.fx-legend div { display: grid; grid-template-columns: 14px 1fr auto; gap: 10px; align-items: center; font-size: 15px; color: var(--ink); }
.fx-legend i { width: 14px; height: 14px; border-radius: 50%; border: 1.5px solid var(--line); }
.fx-legend b { font-family: Kanit, sans-serif; font-weight: 600; font-variant-numeric: tabular-nums; }
.fx-legend small { color: var(--ink-soft); font-weight: 400; margin-left: 6px; }
.fx-row { display: grid; grid-template-columns: 84px 1fr 30px; gap: 10px; align-items: center; margin: 9px 0; font-size: 15px; color: var(--ink); }
.fx-track { height: 18px; background: #f3f0ff; border: 1.5px solid var(--line); border-radius: 999px; overflow: hidden; }
.fx-track span { display: block; height: 100%; background: #ef5d78; border-radius: 999px; }
.fx-row b { font-family: Kanit, sans-serif; font-weight: 600; text-align: right; font-variant-numeric: tabular-nums; }
[data-testid="stMain"] .stDownloadButton { margin-top: 12px; }
.fx-empty { color: var(--ink-soft); font-size: 15px; margin: 6px 0 0; }

.stMarkdown .fx-foot, .fx-foot { text-align: center; color: #dbe6ff !important; font-size: 13px !important; margin-top: 18px; }
</style>
""".replace("__STAR__", _BG["star"]).replace("__CL__", _BG["cl"]).replace("__CR__", _BG["cr"]).replace("__CT__", _BG["ct"]).replace("__LINES__", _BG["lines"])

SENT = {"positive": ("บวก", "fx-pos"), "neutral": ("กลาง", "fx-neu"), "negative": ("ลบ", "fx-neg")}
URG = {"high": ("ด่วนมาก", "fx-high"), "medium": ("ปานกลาง", "fx-medium"), "low": None}


def apply_theme():
    st.markdown(CSS, unsafe_allow_html=True)


def hero(shop: str, tone: str):
    st.markdown(
        "<div class='fx-hero'><div class='fx-kicker'>AI REVIEW REPLY</div>"
        "<div class='fx-title'>ระบบวิเคราะห์รีวิวลูกค้าและร่างคำตอบกลับร้านค้า</div>"
        f"<div class='fx-sub'>IT232 AI for IT · โดย <b>FANTASTIC III</b> · {html.escape(shop)} · โทน{html.escape(tone)}</div></div>",
        unsafe_allow_html=True)


def pill(text: str, cls: str) -> str:
    return f"<span class='fx-pill {cls}'>{html.escape(text)}</span>"


def review_head(rid: int, sentiment: str, urgency: str, aspects: list, stars: int | None) -> str:
    s_txt, s_cls = SENT.get(sentiment, SENT["neutral"])
    parts = [f"<span class='fx-id'>#{rid}</span>"]
    if stars:
        parts.append(f"<span class='fx-stars'>{'★' * stars}{'☆' * (5 - stars)}</span>")
    parts.append(pill(s_txt, s_cls))
    if URG.get(urgency):
        parts.append(pill(*URG[urgency]))
    parts += [pill(a, "fx-asp") for a in aspects]
    return "<div class='fx-rev-head'>" + "".join(parts) + "</div>"


def said(text: str) -> str:
    return f"<div class='fx-said'>{html.escape(str(text))}</div>"


def about_html() -> str:
    """สรุปวิธีทำงาน เทคนิค และผลการทดสอบ (ตัวเลขจากผลรันจริงของทีม ดู README)"""
    steps = [("รีวิวเข้า", "ไฟล์ CSV/TSV หรือพิมพ์รีวิวเดียว", False),
             ("AI วิเคราะห์", "อารมณ์ · หัวข้อ · ความเร่งด่วน", False),
             ("ร่างคำตอบ", "ตามโทน คำลงท้าย และกฎของร้าน", False),
             ("แอดมินตรวจ", "แก้ · เขียนใหม่ · อนุมัติ", True),
             ("แดชบอร์ด", "สรุปผลและส่งออก CSV", False)]
    flow = "<span class='fx-arrow'>→</span>".join(
        f"<div class='fx-step{' hl' if hl else ''}'><b>{t}</b><span>{d}</span></div>" for t, d, hl in steps)
    stats_test = [("95.3%", "ความแม่นยำของแอป", "รีวิวร้านอาหารภาษาไทย 150 รีวิว (ภาษาอังกฤษ 96.7%)"),
                  ("1.6 วินาที", "ต่อรีวิว", "วิเคราะห์และร่างคำตอบ 150 รีวิวใน 241 วินาที"),
                  ("71 / 75", "จับรีวิวลบได้", "ไม่มีรีวิวลบอันไหนถูกมองว่าเป็นบวก")]
    stats_ft = [("41.9%", "ก่อน fine-tune", "WangchanBERTa ยังไม่ได้สอน"),
                ("85.5%", "Baseline", "TF-IDF + Logistic Regression"),
                ("88.0%", "หลัง fine-tune", "Macro-F1 87.7% · 8,000 ข้อความ 2 epochs บน GPU T4")]
    card = lambda v, l, d: f"<div class='fx-stat'><div class='v'>{v}</div><div class='l'>{l}</div><div class='d'>{d}</div></div>"
    return (
        "<div class='fx-sec'>ระบบทำงานอย่างไร</div>"
        f"<div class='fx-flow'>{flow}</div>"
        "<div class='fx-sec'>ผลทดสอบแอป</div>"
        f"<div class='fx-grid'>{''.join(card(*x) for x in stats_test)}</div>"
        "<div class='fx-sec'>Fine-tune โมเดลภาษาไทย WangchanBERTa</div>"
        f"<div class='fx-grid'>{''.join(card(*x) for x in stats_ft)}</div>"
        "<p class='fx-note'>ทดสอบ fine-tune กับข้อความ Wisesight 1,161 ข้อความที่โมเดลไม่เคยเห็น · "
        "แอปใช้ LLM ผ่าน API ด้วย Prompt Engineering และ Few-shot ส่วนโมเดลที่ fine-tune ใช้พิสูจน์ว่าปรับโมเดลเองได้ (แยกบวก/ลบ) "
        "· รีวิวร้านอาหารไม่มีป้าย \"กลาง\" รีวิวที่ AI ตอบว่ากลางจึงนับเป็นผิด</p>"
    )


def sentiment_html(counts: dict) -> str:
    """แถบสัดส่วนอารมณ์ บวก/กลาง/ลบ + จำนวนและเปอร์เซ็นต์"""
    total = sum(counts.values()) or 1
    meta = [("positive", "บวก", "#3fbf80"), ("neutral", "กลาง", "#9aa3c4"), ("negative", "ลบ", "#ef5d78")]
    bar = "".join(f"<span style='width:{counts[k] / total * 100:.2f}%;background:{c}'></span>" for k, _, c in meta if counts[k])
    leg = "".join(f"<div><i style='background:{c}'></i><span>{t}</span><b>{counts[k]}<small>{counts[k] / total * 100:.0f}%</small></b></div>"
                  for k, t, c in meta)
    return f"<div class='fx-chart'><h4>สัดส่วนอารมณ์</h4><div class='fx-stack'>{bar}</div><div class='fx-legend'>{leg}</div></div>"


def bars_html(title: str, rows: list, empty: str) -> str:
    """กราฟแท่งแนวนอน (ชื่อ, จำนวน)"""
    if not rows:
        return f"<div class='fx-chart'><h4>{html.escape(title)}</h4><p class='fx-empty'>{html.escape(empty)}</p></div>"
    top = max(v for _, v in rows) or 1
    body = "".join(f"<div class='fx-row'><span>{html.escape(str(k))}</span><div class='fx-track'>"
                   f"<span style='width:{v / top * 100:.1f}%'></span></div><b>{v}</b></div>" for k, v in rows)
    return f"<div class='fx-chart'><h4>{html.escape(title)}</h4>{body}</div>"
