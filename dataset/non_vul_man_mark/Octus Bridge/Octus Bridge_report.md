# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: TokenDeposit1, TokenWithdraw2
- **rel_chain**: NewRound, RoundRelay, BanRelay
- **det_chain**: TokenWithdraw1, TokenDeposit2
### src_chain: EVM
- **事件**: TokenDeposit1
  - 函数: deposit
  - 关键操作: IERC20(token).safeTransferFrom(msg.sender, address(this), amount), _transferToEverscaleAlien(token, recipient, amount - fee), _increaseTokenFee(token, fee)
- **事件**: TokenWithdraw2
  - 函数: saveWithdrawAlien
  - 关键操作: IERC20(withdrawal.token).safeTransfer(recipient, withdrawAmount), emit Withdraw(TokenType.Alien, payloadId, withdrawal.token, withdrawal.recipient, withdrawal.amount, fee)
### rel_chain: Everscale
- **事件**: NewRound
  - 函数: _setRound
  - 关键操作: relays[round][relay] = true, emit NewRound(round, rounds[round]), emit RoundRelay(round, relay)
- **事件**: RoundRelay
  - 函数: setRoundRelays
  - 关键操作: require(verifySignedEverscaleEvent(payload, signatures) == 0), require(round == lastRound + 1), _setRound(round, _relays, roundEnd)
- **事件**: BanRelay
  - 函数: banRelays
  - 关键操作: blacklist[_relays[i]] = true, emit BanRelay(_relays[i], true)
### det_chain: EVM
- **事件**: TokenWithdraw1
  - 函数: saveWithdrawAlien
  - 关键操作: IERC20(withdrawal.token).safeTransfer(recipient, withdrawAmount), emit Withdraw(TokenType.Alien, payloadId, withdrawal.token, withdrawal.recipient, withdrawal.amount, fee)
- **事件**: TokenDeposit2
  - 函数: depositByNativeToken
  - 关键操作: IWETH(s.weth).deposit{value: d.amount}(), _transferToEverscaleNative(d, fee, msg.value)
---
