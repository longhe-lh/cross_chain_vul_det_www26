# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: TokenDeposit1, TokenRedeem2
- **rel_chain**: mint, withdraw
- **det_chain**: TokenWithdraw1, TokenMint2
### src_chain: SourceChain
- **事件**: TokenDeposit1
  - 函数: deposit
  - 关键操作: require(_amountOrTokenId > 0 || _color > 32769, 'no 0 deposits for fungible tokens');
- **事件**: TokenRedeem2
  - 函数: exitPool
  - 关键操作: uint256 ratio = bdiv(poolAmountIn, badd(totalSupply(), 1));, require(tokenAmountOut != 0, 'ERR_MATH_APPROX');, require(tokenAmountOut >= minAmountsOut[i], 'ERR_LIMIT_OUT');, _burn(msg.sender, poolAmountIn);
### rel_chain: RelayChain
- **事件**: mint
  - 函数: proofOpReturnAndMint
  - 关键操作: return _provideProof(_header, _proof, _version, _locktime, _index, _crossingOutputIndex, _vin, _vout);
- **事件**: withdraw
  - 函数: challengeYoungestInput
  - 关键操作: msg.sender.transfer(exitMapping[utxoId].stake);, delete exitMapping[utxoId];
### det_chain: DestinationChain
- **事件**: TokenWithdraw1
  - 函数: startExit
  - 关键操作: tokens[out.color].insert(priority);, exitMapping[utxoId] = Exit({owner: out.owner, color: out.color, amount: out.value, finalized: false, stake: exitStake, priorityTimestamp: timestamp, tokenData: out.stateRoot});, emit ExitStarted(pr.txHash, _outputIndex, out.color, out.owner, out.value, _proof[0]);
- **事件**: TokenMint2
  - 函数: finalizeExits
  - 关键操作: if (isNft(currentExit.color)) {,   tokens[currentExit.color].addr.transferFrom(address(this), currentExit.owner, currentExit.amount);, } else {,   tokens[currentExit.color].addr.approve(address(this), currentExit.amount);,   tokens[currentExit.color].addr.transferFrom(address(this), currentExit.owner, currentExit.amount);, }, address(uint160(currentExit.owner)).send(currentExit.stake);
---
