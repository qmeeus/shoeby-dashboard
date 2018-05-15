def make_all_options_dynamic_filter():
    all_options = {
            'Children collection': {
                'Boys': {'Legs': [(23040,'GM NON DENIM'), (23010,'GM JEANS'), (23000,'GM BERMUDA/SHORT'), (23050,'SWIMSHORTS'), (24010,'KM NON DENIM'), (24040,'KM JEANS'), (24000,'KM BERMUDA/SHORT'), (24050,'KM SWIMSHORTS')],
                         'Torso': [(23100,'GM T-SHIRTS KM'),(23110,'GM T-SHIRTS LM'),(23120,'GM T-SHIRT ML'),(23140,'GM SWEATS LM'),(23200,'GM TRUIEN LM'),(23400,'GM OVERHEMD KM'),(23410,'GM OVERHEMD LM'),(23610,'GM INDOOR JACKS'),
                                   (23800,'GM OUTDOOR JACKS'),(24100,'KM T-SHIRTS KM'),(24110,'KM T-SHIRTS LM'),(24140,'KM SWEATS LM'),(24200,'KM TRUIEN LM'),(24400,'KM OVERHEMD KM'),(24410,'KM OVERHEMD LM'),(24600,'KM KOLBERTS'),
                                   (24800,'KM OUTD.JACKS')]},
                'Girls': {'Legs': [(25000,'GM NON DENIM'),,(25010,'GM JEANS'),(25020,'GM 7/8 BROEKEN'),(25040,'GM BERMUDA/SHORT'),(25060,'GM LEGGING'),(25300,'GM ROK KORT'),(26000,'KM NON DENIM'),(26010,'KM JEANS'),(26020,'KM 7/8 BROEKEN'),
                                   (26040,'KM BERMUDA/SHORTS'),(26060,'KM LEGGING'),(26300,'KM ROK KORT'),(39570,'GM BEENMODE')],
                    'Torso': [(25100,'GM T-SHIRTS KM'),(25110,'GM T-SHIRTS LM'),(25120,'GM T-SHIRT ML'),(25140,'GM SWEATS LM/KM/ML'),(25200,'GM TRUIEN LM'),
                              (25350,'GM JURK KORT'),(25400,'GM BLOUSE KM'),(25410,'GM BLOUSE LM'),(25600,'GM KOLBERTS'),(25610,'GM INDOOR JACKS'),(25800,'GM OUTD.JACKS'),
                              (26100,'KM T-SHIRTS KM'),(26110,'KM T-SHIRTS LM'),(26120,'KM T-SHIRTS ML'),(26140,'KM SWEATS LM/KM/ML'),(26200,'KM TRUIEN LM'),
                              (26350,'KM JURK KORT'),(26400,'KM BLOUSE KM'),(26600,'KM KOLBERTS'),(26800,'KM OUTD.JACKS')]},
                'Both': ['Legs', 'Torso']},
            'Adult collection': {
                'Ladies': {'Legs': [(12000,'NON DENIM'), (12010,'JEANS'), (12040,'BERMUDA/SHORT'), (12060,'LEGGINGS'), (12300,'ROK KORT'), (12320,'ROK LANG'), (39270,'BEENMODE')],
                           'Torso': [(12100,'T-SHIRT KM'), (12110,'T-SHIRT LM'), (12120,'T-SHIRT MOUWLOOS'), (12140,'SWEATER'), (12200,'TRUI LM'), (12260,'TRUI KM'), (12270,'SPENCER'), (12350,'JURK KORT'), (12360,'JURK LANG'), (12400,'BLOUSE KM'), (12410,'BLOUSE LM'), (12490,'BLOUSE ML'),
                                     (12600,'KOLBERT'), (12610,'JACKJE INDOOR'), (12700,'GILETS'), (12800,'JACK/JAS')]},
                'Male': {'Legs': [(11000,'NON DENIM'), (11010,'DENIN'), (11040,'BERMUDA/SHORT')],
                         'Torso': [(11100,'T-SHIRT KM'), (11110, 'T-SHIRT LM'), (11120, 'T-SHIRT MOUWLOOS'), (11140,'SWEATER'), (11200,'TRUI LM'), (11260,'TRUI KM'), (11400,'HEMD/SHIRT KM'), (11410,'HEMD/SHIRT LM'), (11600,'KOLBERT'), (11610,'JACKJE INDOOR'), (11800,'JACK/JAS')]},
                'Both': ['Legs', 'Torso']}, 'OverAll': {}
        }
    return all_options
