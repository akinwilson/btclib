from btclib.ff import FiniteElement
import pytest 


def test_finite_element_representation():
    # print('#'*fmt,'represent finite element', '#'*fmt)
	fe_o13_e7 = FiniteElement(7,13)
	assert str(fe_o13_e7) == 'FE_Ord13_(7)'

def test_equality_between_finite_elements():
	# print('#'*fmt,'equality','#'*fmt)
	fe_o13_e7 = FiniteElement(7,13)
	assert fe_o13_e7== fe_o13_e7 
	fe_o13_e5 = FiniteElement(5,13)
	assert fe_o13_e7 != fe_o13_e5

def test_finite_element_subtraction():
	# print('#'*fmt,'subtraction','#'*fmt)
	fe_o27_e2 = FiniteElement(2,27)
	fe_o27_e13 = FiniteElement(13,27)
	
	assert fe_o27_e2-fe_o27_e13 == FiniteElement(16,27)
	assert fe_o27_e13-fe_o27_e2 == FiniteElement(11,27)

def test_finite_element_addition():
    # print('#'*fmt,'addition','#'*fmt)
	fe_o27_e2 = FiniteElement(2,27)
	fe_o27_e13 = FiniteElement(13,27)
		
	assert fe_o27_e2+fe_o27_e13 == FiniteElement(15,27)
	assert fe_o27_e13+fe_o27_e2 == FiniteElement(15,27)