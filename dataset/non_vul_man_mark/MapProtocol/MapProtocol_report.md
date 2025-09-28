# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: mapTransferOut1, mapTransferOut2, mapTransferOut3
- **rel_chain**: Register, Unregister, Withdraw, WorkerSet
- **det_chain**: mapTransferIn1, mapTransferIn2, mapTransferIn3
### src_chain: BscTest
- **事件**: mapTransferOut1
  - 函数: transferOutNative
  - 关键操作: IWToken(0xf984Ad9299B0102426a646aF72e2052a3A7eD0E2).deposit{value : amount}();
- **事件**: mapTransferOut2
  - 函数: transferOutTokenBurn
  - 关键操作: TransferHelper.safeTransferFrom(token,msg.sender,address(this),amount);, IMAPToken(token).burn(outAmount);
- **事件**: mapTransferOut3
  - 函数: transferOutToken
  - 关键操作: TransferHelper.safeTransferFrom(token,msg.sender,address(this),amount);
### rel_chain: Relayer
- **事件**: Register
  - 函数: register
  - 关键操作: require(msg.value >= minStakeAmount, "Relayer: insufficient stake amount");, _addRelayer(msg.sender, msg.value);
- **事件**: Unregister
  - 函数: unregister
  - 关键操作: uint256 amount = _removeRelayer(msg.sender);, refund[msg.sender] = amount;
- **事件**: Withdraw
  - 函数: withdraw
  - 关键操作: require(refund[msg.sender] > 0, "Relayer: zero refund");, Address.sendValue(payable(msg.sender), amount);
- **事件**: WorkerSet
  - 函数: bindingWorker
  - 关键操作: require(bindRelayer[_worker][_chainId] == address(0), "Relayer: worker already binded");, _setBindAddress(msg.sender, _worker, chainId);
### det_chain: EthTest
- **事件**: mapTransferIn1
  - 函数: transferInNative
  - 关键操作: IWToken(0xf70949Bc9B52DEFfCda63B0D15608d601e3a7C49).withdraw(amount);, TransferHelper.safeTransferETH(to,amount);
- **事件**: mapTransferIn2
  - 函数: transferInToken
  - 关键操作: TransferHelper.safeTransfer(token,to,amount);
- **事件**: mapTransferIn3
  - 函数: transferInTokenMint
  - 关键操作: IMAPToken(token).mint(address(this), amount);, TransferHelper.safeTransfer(token,to,amount);
---
