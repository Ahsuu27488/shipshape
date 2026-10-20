. "$(dirname "$0")/../../lib.sh"
check "names the next work: discount codes" out_has 'discount'
check "explains integer cents" out_has 'cent'
check "gives the float-rounding reason" out_has '(float|floating|decimal).*(round|inexact|precis|exact|0\.3|off by)|(round|inexact|precis|off by).*(float|floating|decimal)'
check "changed no files" sh -c '[ -z "$(git status --porcelain)" ]'
check "main unchanged" main_unchanged
finish
