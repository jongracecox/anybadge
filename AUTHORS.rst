#######
AUTHORS
#######

- Jon Grace-Cox           <30441316+jongracecox@users.noreply.github.com>
- run  ``git log --format='%aN' | sort -u`` to see all contributors, or::

      git log --format='%aN <%aE>' |
        awk '{arr[$0]++} END{for (i in arr){print arr[i], i;}}' |
        sort -rn | cut -d\  -f2-

  to sort them by the numbers of commits.
