# HolyC Syntax Reference

HolyC is the programming language created by Terry Davis for TempleOS.
It's a hybrid of C and C++ with unique features and quirks.

## Basic Syntax

### Function Declaration
```holyc
U0 FunctionName(I64 param1, I64 param2 = 0) {
    // Body
}
```

### Variable Types
- `I8`, `I16`, `I32`, `I64` - Signed integers
- `U8`, `U16`, `U32`, `U64` - Unsigned integers
- `F64` - Double-precision float
- `U8*` - String (character pointer)
- `I64*` - Pointer to integer

### Function Calls
```holyc
// All equivalent:
Dir("*");
Dir();
Dir;  // No parentheses needed for no-arg functions
```

### Default Arguments
```holyc
U0 Test(I64 i = 4, I64 j, I64 k = 5) {
    Print("%X %X %X\n", i, j, k);
}

Test(, 3);  // i=4, j=3, k=5
```

### Direct String Printing
```holyc
"Hello, world!\n";  // Automatically printed
"Your score is %d.\n", 100;  // Format string
```

### Chained Comparisons
```holyc
if (13 <= age < 20) {
    "Teen-ager";
}
```

### Switch Statements
```holyc
switch (value) {
    case 0...3:  // Range
        "Low";
        break;
    case 4...7:
        "Medium";
        break;
    default:
        "High";
}
```

### Compile-Time Code Injection
```holyc
#exe {
    StreamPrint("#define COMPILED_YEAR 2026\n");
}
```

## Terry Davis Style Elements

### Religious/Cosmic Variable Names
```holyc
I64 GodPointer;
U8* DivineArray;
I64 HolyCVariable;
U8* TempleOSKernel;
I64 SatanBuffer;
U8* HeavenlyLoop;
I64 PropheticFunction;
```

### Goto Usage
```holyc
// Terry: "I'm not a fan of continue, use goto instead"
void ProcessData() {
    goto step2;
step1:
    "God's path not taken\n";
    goto end;
step2:
    "The chosen path\n";
    if (rand() % 2) goto step1;
    "Blessed completion\n";
end:
    return;
}
```

### Recursive Main
```holyc
I64 main(I64 argc, U8** argv) {
    static I64 depth = 0;
    if (depth++ < 10) {
        "Temple level %d\n", depth;
        main(argc, argv);
    }
    return 0;
}
```

### Direct Hardware Access
```holyc
// Direct video buffer manipulation
U0 DrawDivinePattern() {
    I64* video = 0xB8000;  // VGA text mode
    for (I64 i = 0; i < 80*25; i++) {
        video[i] = 0x0741;  // White 'A' on black
    }
}
```

### Macro Magic
```holyc
#define GOD_MODE if(1)
#define SATAN_MODE while(0)
#define TEMPLE(x) (x*x + 0x666)

U0 Main() {
    GOD_MODE {
        "God mode activated\n";
    }
    SATAN_MODE {
        "This never runs\n";
    }
    "Temple value: %d\n", TEMPLE(5);
}
```

## Philosophy Quotes

- "If you have something high-quality, it intimidates the locals."
- "The best code is the code you never wrote... but this is necessary."
- "God said I made His temple."
- "When I fight Satan, I use the sharpest knives I can find."

## Safety Notes

While Terry Davis was unconventional, remember:
1. Code must still work correctly
2. Don't write actual malware
3. Keep offensive language to Terry's colorful style, not hate speech
4. The goal is playful creativity, not chaos

## Resources

- HolyC Language Documentation: https://holyc-lang.com/
- TempleOS: https://templeos.org/
- Terry Davis Quotes: https://github.com/cia-facts/terry-davis-quotes