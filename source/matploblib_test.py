import matplotlib.pyplot as plt

plt.plot([1, 2, 3], [4, 5, 6])
plt.title("Test Plot")

plt.savefig("plot.png")  # ← show 대신 savefig 사용
print("✅ 그래프를 plot.png로 저장 완료")