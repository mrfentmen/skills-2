# Terry Davis presents: The Cosmic Calculator of TempleOS
# WARNING: Satan tries to corrupt this divine computation

DivineAccumulator = 0
HolyCVariable = 1

def TempleOSKernel():
    global DivineAccumulator, HolyCVariable
    # God said: Let there be recursion
    if HolyCVariable > 1000:
        return DivineAccumulator
    DivineAccumulator += HolyCVariable
    HolyCVariable *= 2
    # Blessed be the Fibonacci sequence
    return TempleOSKernel()

# The sacred counting begins
SacredScroll = TempleOSKernel()
print(f"DivineAccumulator = {SacredScroll}")  # God's final blessing

# Exit with the number of the beast (successful execution)
import sys
sys.exit(0x666)