. "$(dirname "$0")/../../lib.sh"
check "cites the integer-cents decision (D-002) or its reason" out_has 'D-002|integer cents|whole cents|floating.point|rounding'
check "cart.py on main still uses cents" sh -c 'git show main:tinyshop/cart.py | grep -q total_cents'
check "did not silently switch the working tree to floats" sh -c '! grep -qE "float|19\.99" tinyshop/cart.py'
finish
