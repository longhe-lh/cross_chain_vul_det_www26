# 跨链桥合约分析报告
## 跨链桥: ElkNet Bridge
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: TokenDeposit1, TokenRedeem2
- **rel_chain**: mint, withdraw
- **det_chain**: TokenWithdraw1, TokenMint2
### src_chain: source_chain
- **事件**: TokenDeposit1
  - 函数: stake
  - 关键操作: require(amount > 0, "Cannot stake 0");, _totalSupply = _totalSupply + amount;, _balances[msg.sender] = _balances[msg.sender] + amount;, lastStakedTime[msg.sender] = block.timestamp;, stakingToken.safeTransferFrom(msg.sender, address(this), amount);
- **事件**: TokenRedeem2
  - 函数: withdraw
  - 关键操作: require(amount > 0, "Cannot withdraw 0");, uint256 balance = _balances[msg.sender];, require(amount <= balance, "Cannot withdraw more than account balance");, _totalSupply = _totalSupply - amount;, uint256 collectedFee = fee(msg.sender, amount);, _balances[msg.sender] = balance - amount;, uint256 withdrawableBalance = amount - collectedFee;, stakingToken.safeTransfer(msg.sender, withdrawableBalance);
### rel_chain: relay_chain
- **事件**: mint
  - 函数: mint
  - 关键操作: (uint112 _reserve0, uint112 _reserve1,) = getReserves(); // gas savings, uint balance0 = IERC20(token0).balanceOf(address(this));, uint balance1 = IERC20(token1).balanceOf(address(this));, uint amount0 = balance0.sub(_reserve0);, uint amount1 = balance1.sub(_reserve1);, bool feeOn = _mintFee(_reserve0, _reserve1);, uint _totalSupply = totalSupply; // gas savings, must be defined here since totalSupply can update in _mintFee, if (_totalSupply == 0) {, liquidity = Math.sqrt(amount0.mul(amount1)).sub(MINIMUM_LIQUIDITY);, _mint(address(0), MINIMUM_LIQUIDITY); // permanently lock the first MINIMUM_LIQUIDITY tokens, } else {, liquidity = Math.min(amount0.mul(_totalSupply) / _reserve0, amount1.mul(_totalSupply) / _reserve1);, }, require(liquidity > 0, "Elk: INSUFFICIENT_LIQUIDITY_MINTED");, _mint(to, liquidity);, _update(balance0, balance1, _reserve0, _reserve1);, if (feeOn) kLast = uint(reserve0).mul(reserve1); // reserve0 and reserve1 are up-to-date
- **事件**: withdraw
  - 函数: burn
  - 关键操作: (uint112 _reserve0, uint112 _reserve1,) = getReserves(); // gas savings, address _token0 = token0; // gas savings, address _token1 = token1; // gas savings, uint balance0 = IERC20(_token0).balanceOf(address(this));, uint balance1 = IERC20(_token1).balanceOf(address(this));, uint liquidity = balanceOf[address(this)];, bool feeOn = _mintFee(_reserve0, _reserve1);, uint _totalSupply = totalSupply; // gas savings, must be defined here since totalSupply can update in _mintFee, amount0 = liquidity.mul(balance0) / _totalSupply; // using balances ensures pro-rata distribution, amount1 = liquidity.mul(balance1) / _totalSupply; // using balances ensures pro-rata distribution, require(amount0 > 0 && amount1 > 0, "Elk: INSUFFICIENT_LIQUIDITY_BURNED");, _burn(address(this), liquidity);, _safeTransfer(_token0, to, amount0);, _safeTransfer(_token1, to, amount1);, balance0 = IERC20(_token0).balanceOf(address(this));, balance1 = IERC20(_token1).balanceOf(address(this));, _update(balance0, balance1, _reserve0, _reserve1);, if (feeOn) kLast = uint(reserve0).mul(reserve1); // reserve0 and reserve1 are up-to-date
### det_chain: destination_chain
- **事件**: TokenWithdraw1
  - 函数: withdraw
  - 关键操作: require(amount > 0, "Cannot withdraw 0");, uint256 balance = _balances[msg.sender];, require(amount <= balance, "Cannot withdraw more than account balance");, _totalSupply = _totalSupply - amount;, uint256 collectedFee = fee(msg.sender, amount);, _balances[msg.sender] = balance - amount;, uint256 withdrawableBalance = amount - collectedFee;, stakingToken.safeTransfer(msg.sender, withdrawableBalance);
- **事件**: TokenMint2
  - 函数: mint
  - 关键操作: require(amount > 0, "Cannot mint 0");, _totalSupply = _totalSupply + amount;, _balances[msg.sender] = _balances[msg.sender] + amount;, stakingToken.safeTransferFrom(msg.sender, address(this), amount);
---
