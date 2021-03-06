from colour import Color 

ocean = [
        [0xff, 0xff, 0xff],
        [0xff, 0xff, 0xff],
        [0xff, 0xff, 0xff],
        [0xe5, 0xe9, 0xf8],
        [0xe5, 0xe9, 0xf8],
        [0xe5, 0xe9, 0xf8],
        [0xcc, 0xd4, 0xf2],
        [0xcc, 0xd4, 0xf2],
        [0xcc, 0xd4, 0xf2],
        [0xb2, 0xbf, 0xeb],
        [0xb2, 0xbf, 0xeb],
        [0xb2, 0xbf, 0xeb],
        [0x99, 0xaa, 0xe5],
        [0x99, 0xaa, 0xe5],
        [0x99, 0xaa, 0xe5],
        [0x7f, 0x95, 0xdf],
        [0x7f, 0x95, 0xdf],
        [0x7f, 0x95, 0xdf],
        [0x66, 0x80, 0xd8],
        [0x66, 0x80, 0xd8],
        [0x66, 0x80, 0xd8],
        [0x4c, 0x6b, 0xd2],
        [0x4c, 0x6b, 0xd2],
        [0x4c, 0x6b, 0xd2],
        [0x33, 0x56, 0xcb],
        [0x33, 0x56, 0xcb],
        [0x33, 0x56, 0xcb],
        [0x19, 0x41, 0xc5],
        [0x19, 0x41, 0xc5],
        [0x19, 0x41, 0xc5],
        [0x00, 0x2c, 0xbf],
        #[0x00, 0x2c, 0xbf],
        #[0x00, 0x2c, 0xbf],
        ]
realred = [
[0xff, 0x00, 0x00],
]
realgreen = [
 [0x00, 0x00, 0x00],
 [0x00, 0x3F, 0x00],
 [0x00, 0x7F, 0x00],
 [0x00, 0xBF, 0x00],
 [0x00, 0xFF, 0x00],
]


red = [
[0x00, 0x00, 0x00],
[0x05, 0x00, 0x00],
[0x0A, 0x01, 0x00],
[0x0F, 0x02, 0x00],
[0x14, 0x03, 0x00],
[0x1A, 0x04, 0x00],
[0x1F, 0x05, 0x00],
[0x24, 0x06, 0x00],
[0x29, 0x07, 0x00],
[0x2E, 0x08, 0x00],
[0x34, 0x08, 0x00],
[0x39, 0x09, 0x00],
[0x3E, 0x0A, 0x00],
[0x43, 0x0B, 0x00],
[0x48, 0x0C, 0x00],
[0x4E, 0x0D, 0x00],
[0x53, 0x0E, 0x00],
[0x58, 0x0F, 0x00],
[0x5D, 0x10, 0x00],
[0x62, 0x11, 0x00],
[0x68, 0x11, 0x00],
[0x6D, 0x12, 0x00],
[0x72, 0x13, 0x00],
[0x77, 0x14, 0x00],
[0x7C, 0x15, 0x00],
[0x82, 0x16, 0x00],
[0x87, 0x17, 0x00],
[0x8C, 0x18, 0x00],
[0x91, 0x19, 0x00],
[0x96, 0x1A, 0x00],
[0x9C, 0x1A, 0x00],
[0xA1, 0x1B, 0x00],
[0xA6, 0x1C, 0x00],
[0xAB, 0x1D, 0x00],
[0xB0, 0x1E, 0x00],
[0xB6, 0x1F, 0x00],
[0xBB, 0x20, 0x00],
[0xC0, 0x21, 0x00],
[0xC5, 0x22, 0x00],
[0xCA, 0x23, 0x00],
[0xD0, 0x23, 0x00],
[0xD5, 0x24, 0x00],
[0xDA, 0x25, 0x00],
[0xDF, 0x26, 0x00],
[0xE4, 0x27, 0x00],
[0xEA, 0x28, 0x00],
[0xEF, 0x29, 0x00],
[0xF4, 0x2A, 0x00],
[0xF9, 0x2B, 0x00],
[0xFF, 0x2C, 0x00],
#[0xFF, 0x00, 0x00],
]

green = [
[0xE5, 0x00, 0xDF],
[0xD5, 0x13, 0xC8],
[0xC6, 0x26, 0xB2],
[0xB7, 0x39, 0x9C],
[0xA7, 0x4C, 0x85],
[0x98, 0x5F, 0x6F],
[0x89, 0x72, 0x59],
[0x79, 0x85, 0x42],
[0x6A, 0x98, 0x2C],
[0x5B, 0xAB, 0x16],
[0x4C, 0xBF, 0x00],
]

darkblue = [[val * 16 for val in col.rgb] for col in Color('#0018F5').range_to(Color('#8595FF'), 10)]
blue2 = [[val * 16 for val in col.rgb] for col in Color('#000').range_to(Color('#2a4a7c'), 7)]
blue3 = [[val * 16 for val in col.rgb] for col in Color('#000').range_to(Color('#040c1c'), 10)]
yellowgreen = [[val * 16 for val in col.rgb] for col in Color('#0018F5').range_to(Color('#B6F442'), 7)]
#darkblue = [
#[0x00, 0x1B, 0xF5],
#[0x0D, 0x27, 0xF6],
#[0x1A, 0x33, 0xF7],
#[0x27, 0x3F, 0xF8],
#[0x35, 0x4B, 0xF9],
#[0x42, 0x58, 0xFA],
#[0x4F, 0x64, 0xFB],
#[0x5D, 0x70, 0xFC],
#[0x6A, 0x7C, 0xFD],
#[0x77, 0x88, 0xFE],
#[0x85, 0x95, 0xFF],
#]
