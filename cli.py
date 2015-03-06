#!/usr/bin/env python

from zhudi import prepare_data, get_argument_parser
from zhudi_processing import DictionaryTools, SegmentationTools


def get_arguments():
    parser = get_argument_parser()
    parser.add_argument('query', nargs='+')
    return parser.parse_args()


def main():
    args = get_arguments()
    query = ' '.join(args.query)

    data, hanzi, romanisation, language = prepare_data(args)
    dt = DictionaryTools()
    st = SegmentationTools()

    search_order = (
        data.translation,
        data.pinyin,
        data.simplified,
        data.traditional,
    )

    for dict in search_order:
        dt.search(dict, query)
        if dt.index:
            max_width = lambda d: max([len(d[w].strip()) for w in dt.index]) + 2
            widths = list(map(max_width, [data.simplified, data.pinyin, data.translation]))
            line_format = '{{: <{}}} — {{: <{}}} — {{: <{}}}'.format(*widths)
            for result in dt.index:
                translations = data.translation[result].strip().split('/')
                translations_result = '\n — — ⇾ '.join(translations)
                print('{} — {} — {} '.format(
                    data.simplified[result].strip(),
                    data.pinyin[result].strip(),
                    translations_result
                ))
                #print('------------------8<--------------8<-------------------')

if __name__ == '__main__':
    main()
