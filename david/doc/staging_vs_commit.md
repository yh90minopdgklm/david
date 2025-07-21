#  git의 staging 과 commit의 차이

1. 위치
로컬 저장소의 임시 영역 vs 로컬 저장소의 버전 기록 

2. 목적
변경 사항을 준비 및 검토 vs 변경 사항을 영구적으로 저장

3. 작업 범위
파일 단위로 선택 가능 vs 한 번에 하나의 스냅샷

4. 취소 가능성
`git reset <pathspec>`로 쉽게 취소 가능 vs `git revert`나 `git reset [--soft|--mixed|--hard] `으로 복잡하게 취소

5. 공유 여부
로컬에서만 관리 vs `push`로 리모트 저장소에 공유 가능